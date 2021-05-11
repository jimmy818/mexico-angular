from django.db import transaction
from django.shortcuts import  get_object_or_404
from django_filters import rest_framework as filters
from django.utils.decorators import method_decorator
from django.db.transaction import atomic
from django.utils.translation import ugettext as _
from rest_framework import filters as df, mixins, status, viewsets
from rest_framework import exceptions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import Response, status, APIView

from . import filters as filter_catalog, models, serializers, tasks
from . import utils
from . import mixins

from apps.security import serializers as serializers_user
import xlrd
import datetime
import copy


class LevelCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.LevelCategorySerializer
    queryset = models.CategoryLevel.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    # filterset_fields = ('name',)
    search_fields = ('name',)

    def get_queryset(self):
        return self.queryset.filter(active=True).order_by('id')


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('category_level',)
    search_fields = ('name',)

    def get_queryset(self):
        return self.queryset.filter(active=True).order_by('id')

    def get_serializer_class(self):
        if self.action == 'subcategories':
            return serializers.SubCategorySerializer
        return self.serializer_class

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['get'])
    def subcategories(self, request, pk=None):
        category = self.get_object()
        serializer = self.get_serializer(category.subcategory_set.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.SubCategorySerializer
    queryset = models.SubCategory.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('category',)
    search_fields = ('name', 'category__name',)

    def get_queryset(self):
        return self.queryset.filter(active=True).order_by('id')

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


class BlockExerciceView(mixins.CreateListMixin, viewsets.ModelViewSet):
    queryset = models.ExerciseBlock.objects.all()
    serializer_class = serializers.ExerciceBlockSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('active','created_by','institution','active','has_library','exercise__sub_category__category__category_level')
    search_fields = ('exercise__english_name', 'exercise__spanish_name',)

    def get_serializer_class(self):
        if self.action == 'list':
            return serializers.ExerciseBlockDetailSerializer
        return self.serializer_class
    
    def perform_create(self, serializer):
        item = serializer.save()
        return item
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = serializers.ExerciceBlockMediaSerializer(instance,many=True)
        return Response(instance_serializer.data)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.block_exercice_library(instance,request,True)

        return Response(status=status.HTTP_201_CREATED)
    
    @action(["post"], detail=True)
    @transaction.atomic
    def copy_to_block(self, request, pk=None):
        instance = self.get_object()
        block = get_object_or_404(models.Block,pk=int(self.request.data.get('block'))) 
        tasks.block_exercice_library(instance,request,False,block)

        return Response(status=status.HTTP_201_CREATED)



class ExcercicesViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExcerciceSerializer
    queryset = models.Exercise.objects.order_by('?')
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.ExerciseFilter
    filterset_fields = ('sub_category','created_by','created_by__institution','active','has_library','request_library')
    search_fields = ('english_name', 'spanish_name',)
    ordering_fields = ['english_name', 'spanish_name', 'created_at', 'updated_at']

    # def get_queryset(self):
    #     sub_category = self.request.GET.get("sub_category")
    #     if sub_category:
    #         print(sub_category)
    #         return models.Exercise.objects.filter(sub_category__in=sub_category.split(','))
    #     return super().get_queryset()
    
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        media = request.data.pop('media', None)

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)

        if media:
            media['exercise'] = instance.id
            media_serializer = serializers.MediaExerciceModelSerializer(data=media)
            media_serializer.is_valid(raise_exception=True)
            mediaexercice = media_serializer.save() 

        exercise = self.get_serializer(instance)
        return Response(exercise.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        item = serializer.save(
            created_by=self.request.user
        )
        return item

    @transaction.atomic
    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if instance.has_library:
            raise exceptions.ValidationError(_('You cannot modify a preloaded exercise on the site.'))

        media = request.data.pop('media', None)

        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        if media:
            try:
                mediaexercice = models.MediaExercice.objects.get(exercise=instance)
                media_serializer = serializers.MediaExerciceModelSerializer(mediaexercice, data=media, partial=True, context={'request': request})
                media_serializer.is_valid(raise_exception=True)
                media_serializer.save()
            except models.MediaExercice.DoesNotExist:
                media['exercise'] = instance.id
                media_serializer = serializers.MediaExerciceModelSerializer(data=media)
                media_serializer.is_valid(raise_exception=True)
                media_serializer.save()

        exercise = self.get_serializer(instance)        
        return Response(exercise.data)
    
    def destroy(self, request, pk=None):
        instance = self.get_object()

        if instance.has_library:
            raise exceptions.ValidationError(_('You cannot delete a preloaded exercise on the site.'))

        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ExerciceImageView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.ExcerciceMediaSerializer  
    queryset = models.Exercise.objects.all().distinct()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.ExerciseFilter
    filterset_fields = ('sub_category','sub_category__category','sub_category__category__category_level')

# @method_decorator(atomic, name='dispatch')
class ExcelCategory(APIView):
    def post(self, request):
        input_excel = request.FILES['excel']
        book = xlrd.open_workbook(file_contents=input_excel.read())
        # sheets = book.sheet_names()
        sheet_0 = book.sheet_by_index(0) # Open the first tab
        sub_cat = []
        total = []
        total_s = []
        start_cat = None
        start_subcat = None
        sub_cat_s = []
        for row_index in range(2):
            for col_index in range(sheet_0.ncols):
                '''
                This function define col starts [1,1] = category  and ends Clean
                '''
                if col_index > 0 and row_index != 0 and col_index <= 187:
                    # dad_last = sheet_0.cell(rowx= 0 ,colx=col_index).value
                    category = sheet_0.cell(rowx=row_index,colx=col_index).value

                    if start_cat == None:
                        start_cat = category
                        start_cat = start_cat.strip()
                        upper_cat = start_cat.upper().replace(" ", "")
                    elif start_cat != category and len(str(category)) != 0:
                        start_cat = start_cat.strip()
                        upper_cat = start_cat.upper().replace(" ", "")
                        catego = {
                            "catalog_dad": utils.get_new_cat_father(sheet_0,col_index - 1),
                            "category" : start_cat,
                            "upper_category" : upper_cat,
                            "sub_categories" : sub_cat
                        }
                        total.append(catego)
                        sub_cat = []
                        start_cat = category
                    data = {
                        "name" : sheet_0.cell(rowx=row_index + 1,colx=col_index).value,
                        "code" : sheet_0.cell(rowx=row_index + 2,colx=col_index).value
                    }
                    sub_cat.append(data)
                    '''
                    Last after sub sub categories
                    '''
                    if col_index == 187:
                        start_cat = start_cat.strip()
                        upper_cat = start_cat.upper().replace(" ", "")
                        catego = {
                            "catalog_dad": utils.get_new_cat_father(sheet_0,col_index - 1),
                            "category" : start_cat,
                            "upper_category" : upper_cat,
                            "sub_categories" : sub_cat
                        }
                        total.append(catego)
                        sub_cat = []
                        start_cat = category
                elif col_index > 0 and row_index != 0 and col_index >= 188 and col_index < 241:
                    category = sheet_0.cell(rowx=row_index,colx=col_index).value
                    if start_subcat == None:
                        start_subcat = category
                        start_subcat = start_subcat.strip()
                        start_subcat = start_subcat.upper().replace(" ", "")
                    elif start_subcat != category and len(str(category)) != 0:
                        start_subcat = start_subcat.strip()
                        upper_cat = start_subcat.upper().replace(" ", "")
                        catego = {
                            "dad": utils.get_dad(col_index),
                            "category" : start_subcat,
                            "upper_category" : upper_cat,
                            "sub_categories" : sub_cat_s
                        }
                        total_s.append(catego)
                        sub_cat_s = []
                        start_subcat = category
                    data = {
                        "name" : sheet_0.cell(rowx=row_index + 1,colx=col_index).value,
                        "code" : sheet_0.cell(rowx=row_index + 2,colx=col_index).value
                    }
                    sub_cat_s.append(data)
                    '''
                    End sub sub categories
                    '''
                    if col_index == 239:
                        start_subcat = start_subcat.strip()
                        upper_cat = start_subcat.upper().replace(" ", "")
                        catego = {
                            "dad" : utils.get_dad(col_index),
                            "category" : start_subcat,
                            "upper_category" : upper_cat,
                            "sub_categories" : sub_cat_s
                        }
                        total_s.append(catego)
                        sub_cat_s = []
                        start_subcat = category
        print('hola mundo')

        utils.add_data_categories(total)
        print('hola mundo')
        utils.add_data_subcategories(total_s)
        return Response(total,status=status.HTTP_200_OK)

@method_decorator(atomic, name='dispatch')
class ExcelExcercices(APIView):
    def post(self, request):
        input_excel = request.FILES['excel']
        book = xlrd.open_workbook(file_contents=input_excel.read())
        # sheets = book.sheet_names()
        sheet_0 = book.sheet_by_index(0) # Open the first tab
        ## this range is for excercices length
        for row_index in range(1012):
            if row_index > 3:
                
                excercice = None
                for col_index in range(sheet_0.ncols):
                    item = sheet_0.cell(rowx=row_index,colx=col_index).value
                    if excercice == None:
                        excercice = item
                        excercice_item = utils.get_or_add_excercice(excercice,self.request.user)
                    else:
                        if item != None and item != '':
                            utils.add_sub_excercice(excercice_item,sheet_0.cell(rowx=3,colx=col_index).value)
                            print(excercice)
                            print(sheet_0.cell(rowx=3,colx=col_index).value)
        return Response(status=status.HTTP_200_OK)


class ProgramViewSet(viewsets.ModelViewSet):
    queryset = models.Program.objects.all().filter(active=True)
    serializer_class = serializers.ProgramSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('has_library',)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ProgramRetrieveSerializer
        if self.action == 'phases':
            return serializers.ProgramPhasesSerializer
        return self.serializer_class

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        instance_serializer = serializers.ProgramRetrieveSerializer(instance, context={'request': request})
        return Response(instance_serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        return instance

    # def destroy(self, request, pk=None):
    #     instance = self.get_object()
    #     instance.active = False
    #     instance.save()

    #     return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.program_as_library(instance)

        return Response(status=status.HTTP_201_CREATED)

    @action(["get"], detail=True)
    def phases(self, request, pk=None):
        program = self.get_object()
        serializer = self.get_serializer(
            program.program_phase.filter(active=True), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhaseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PhaseSerializer
    queryset = models.Phase.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('program', 'has_library',)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'weeks':
            return serializers.PhaseWeekSerializer
        return self.serializer_class

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        phase = serializers.PhasesRetrieveSerializer(instance)
        return Response(phase.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        programa = instance.program
        phases = programa.program_phase.filter(active=True).exclude(id=instance.id).order_by('order')
        for idx, phase in enumerate(phases):
            phase.order = idx + 1
            phase.save()

        return super(PhaseViewSet, self).destroy(request, *args, **kwargs)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.phase_as_library(instance)

        return Response(status=status.HTTP_201_CREATED)

    @action(["get"], detail=True)
    def weeks(self, request, pk=None):
        phase = self.get_object()
        serializer = self.get_serializer(
            phase.phase_week.filter(active=True).order_by('order'), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PhaseSorting(APIView):
    queryset = models.Program.objects.all()

    @transaction.atomic
    def post(self, request, program):
        program = get_object_or_404(models.Program, pk=program)
        phases = request.data

        start_phase = None        
        end_phase = None

        for idx, item in enumerate(phases):
            pk = item.get('id', None)
            phase = get_object_or_404(models.Phase, pk=pk)

            starts = item.get('starts', None)
            if not starts:
                raise exceptions.ValidationError(_('New start date on phase is required'))

            starts = datetime.datetime.strptime(starts, '%Y-%m-%d') # str to date object
            lastDay = None # aux var
            weeks = phase.phase_week.filter(active=True).order_by('order')

            # Validacion para recorrer una fase si otra se superpone a ella
            if start_phase and end_phase:
                if start_phase.date() <= starts.date() <= end_phase:
                    starts = end_phase + datetime.timedelta(days=1)
                    starts = datetime.datetime.strptime(str(starts), '%Y-%m-%d')

            last_end = None
            for idy, item in enumerate(weeks):
                if not idy:
                    start_phase = starts

                if lastDay:
                    days = abs(lastDay-item.starts).days
                    # caculating the weeks, // = floor division operator
                    add = days//7
                    starts = starts + datetime.timedelta(weeks=add)

                lastDay = item.starts

                year, week, weekday = utils.get_year_and_week(starts)
                start, end = utils.get_start_end_dates(year, week)

                item.number_week = week
                item.starts = start
                item.ends = end
                item.order = (idy + 1)
                item.save()
                last_end = end

            lastDay = None
            phase.order = (idx + 1)
            phase.save()

            end_phase = last_end

        serializer = serializers.ProgramRetrieveSerializer(program, context={'request': request})
        return Response(serializer.data, status=200)


class CreateAndMovePhases(APIView):
    queryset = models.Phase.objects.all()

    @transaction.atomic
    def post(self, request):
        data = request.data
        serializer = serializers.PhaseSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        phase = serializer.save()

        program = phase.program
        count = phase.phase_week.filter(active=True).count()

        phases = program.program_phase.filter(active=True).order_by('order')
        move = False
        for idx, _phase in enumerate(phases):
            if _phase.id == phase.id:
                move = True
            else:
                if move and count:
                    weeks = _phase.phase_week.filter(active=True).order_by('order')
                    for idy, _week in enumerate(weeks):
                        start = _week.starts + datetime.timedelta(weeks=(count - 1))
                        year, week, weekday = utils.get_year_and_week(start)
                        start, end = utils.get_start_end_dates(year, week)

                        _week.number_week = week
                        _week.starts = start
                        _week.ends = end
                        _week.order = idy + 1
                        _week.save()

        serializer = serializers.ProgramRetrieveSerializer(program, context={'request': request})
        return Response(serializer.data, status=200)


class DeleteAndMovePhases(APIView):
    queryset = models.Phase.objects.all()

    @transaction.atomic
    def delete(self, request, pk):
        instance = get_object_or_404(models.Phase, pk=pk)
        program = instance.program

        count = instance.phase_week.filter(active=True).count()
        phases = program.program_phase.filter(active=True).order_by('order')

        move = False
        for idx, _phase in enumerate(phases):
            if _phase.id == instance.id:
                _phase.delete()
                move = True
            else:
                if move and count:
                    weeks = _phase.phase_week.filter(active=True).order_by('order')
                    for idy, _week in enumerate(weeks):
                        start = _week.starts - datetime.timedelta(weeks=count)
                        year, week, weekday = utils.get_year_and_week(start)
                        start, end = utils.get_start_end_dates(year, week)

                        _week.number_week = week
                        _week.starts = start
                        _week.ends = end
                        _week.order = idy + 1
                        _week.save()

                    _phase.order = _phase.order - 1
                    _phase.save()

        serializer = serializers.ProgramRetrieveSerializer(program, context={'request': request})
        return Response(serializer.data, status=200)


class WeekViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeekSerializer
    queryset = models.Week.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('phase', 'active', 'has_library',)
    search_fields = ('name',)

    def get_serializer_class(self):
        if self.action == 'days':
            return serializers.DaySerializer
        return self.serializer_class

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.week_as_library(instance)
        return Response(status=status.HTTP_201_CREATED)

    @action(["get"], detail=True)
    def days(self, request, pk=None):
        week = self.get_object()
        serializer = self.get_serializer(week.week_day.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WeekPhaseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WeekPhaseSerializer
    queryset = models.Week.objects.all().order_by('-number_week')
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('phase', 'active', 'has_library',)
    search_fields = ('name',)

    @transaction.atomic
    def perform_create(self, serializer):
        user = self.request.user
        validate_week = utils.validate_week_phase(self.request.data.get('phase'),self.request.data.get('number_week'))
        validate_name = utils.validate_week_name(self.request.data.get('phase'),self.request.data.get('name'))
        if validate_week:
            print(validate_week.id)
            raise exceptions.ValidationError(_('week is used in this phase'))
        if validate_name:
            raise exceptions.ValidationError(_('name week in this phase is used'))
        item = serializer.save(
            active=True
        )
        return item
    
    @transaction.atomic
    def perform_update(self, serializer):
        user = self.request.user
        validate_week = utils.validate_week_phase_update(self.request.data.get('phase'),self.request.data.get('number_week'),self.kwargs.get('pk'))
        validate_name = utils.validate_week_name_update(self.request.data.get('phase'),self.request.data.get('name'),self.kwargs.get('pk'))
        if validate_week:
            raise exceptions.ValidationError(_('week is used in this phase'))
        if validate_name:
            raise exceptions.ValidationError(_('name week in this phase is used'))
        item = serializer.save(
            active=True
        )
        return item
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        phases = instance.phase
        weeks = phases.phase_week.filter(active=True).exclude(id=instance.id).order_by('order')
        for idx, week in enumerate(weeks):
            week.order = idx + 1
            week.save()

        return super(WeekPhaseViewSet, self).destroy(request, *args, **kwargs)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.day_as_library(instance)

        return Response(status=status.HTTP_201_CREATED)


class WeeksSorting(APIView):
    queryset = models.Phase.objects.all()

    @transaction.atomic
    def post(self, request, phase):
        phase = models.Phase.objects.get(id=phase)
        weeks = request.data
        for idx, week in enumerate(weeks):
            id = week.get('id')
            number_week = week.get('number_week')
            year = week.get('year')
            order = week.get('order')

            instance = models.Week.objects.get(id=id)

            # if idx > 0:
            #     if models.Week.objects.filter(
            #         Q(phase=phase, number_week=number_week) |
            #         Q(phase=phase, order=order)).exclude(id=instance.id).exists():
            #         raise exceptions.ValidationError(_('number_week or order in this phase are duplicated')) 

            if instance.active:
                instance.number_week = number_week
                starts, ends = utils.start_end_days_of_week(year, number_week)
                instance.starts = starts
                instance.ends = ends
                instance.order = order
                instance.save()

        serializer = serializers.PhaseWeekSerializer(
            phase.phase_week.filter(active=True).order_by('order'), many=True)

        return Response(serializer.data, status=200)


class ArrayWeeksSorting(APIView):
    queryset = models.Phase.objects.all()

    @transaction.atomic
    def post(self, request, phase):
        phase = models.Phase.objects.get(id=phase)
        weeks = request.data

        qs_weeks = models.Week.objects.filter(id__in=weeks).order_by('number_week')
        data = []
        for week in qs_weeks:
            year = week.starts.year
            data.append({                
                "number_week": week.number_week,
                "starts": week.starts,
                "ends": week.ends
            })

        for idx, week in enumerate(weeks):
            instance = get_object_or_404(models.Week, pk=week)
            instance.number_week = data[idx]["number_week"]
            instance.starts = data[idx]["starts"]
            instance.ends = data[idx]["ends"]
            instance.order = idx + 1
            instance.save()

        serializer = serializers.WeeksRetrieveSerializer(
            phase.phase_week.filter(active=True).order_by('order'), many=True)

        return Response(serializer.data, status=200)

class ArrayWorkoutksSorting(APIView):

    @transaction.atomic
    def post(self, request,day):
        weeks = request.data
        for idx, week in enumerate(weeks):
            instance = get_object_or_404(models.Workout, pk=week)
            instance.order = idx + 1
            instance.day = get_object_or_404(models.Day, pk=day)
            instance.save()

        return Response(status=204)

class ArrayBlocksSorting(APIView):

    @transaction.atomic
    def post(self, request,workout):
        blocks = request.data
        for idx, block in enumerate(blocks):
            instance = get_object_or_404(models.Block, pk=block)
            instance.order = idx + 1
            instance.workout = get_object_or_404(models.Workout, pk=workout)
            instance.save()

        return Response(status=204)


class CopyWeeks(APIView):
    queryset = models.Week.objects.all()

    @transaction.atomic
    def post(self, request, pk):
        data = request.data
        user = request.user
        instance = get_object_or_404(models.Week, pk=pk)

        new_week = copy.deepcopy(instance)
        new_week.pk = None
        new_week.save()

        _start = instance.ends + datetime.timedelta(days=1)
        year, week, weekday = utils.get_year_and_week(_start)
        starts, ends = utils.get_start_end_dates(year, week)

        new_week.number_week = week
        new_week.starts = starts
        new_week.ends = ends
        new_week.save()

        for day in instance.week_day.all().order_by('day'):
            utils.copy_day(user, day, new_week)

        phase = new_week.phase
        program = phase.program

        phases = program.program_phase.filter(active=True, has_library=False).order_by('order')
        move = False
        for idx, _phase in enumerate(phases):
            if _phase.id == phase.id:
                weeks = _phase.phase_week.filter(active=True, has_library=False).order_by('order', 'created_at')
                for idy, _week in enumerate(weeks):
                    if _week.id == new_week.id:
                        _week.order = idy + 1
                        _week.save()
                        move = True
                    else:
                        if move:
                            start = _week.starts + datetime.timedelta(weeks=1)
                            year, week, weekday = utils.get_year_and_week(start)
                            start, end = utils.get_start_end_dates(year, week)

                            _week.number_week = week
                            _week.starts = start
                            _week.ends = end
                            _week.order = idy + 1
                            _week.save()
                        else:
                            _week.order = idy + 1
                            _week.save()
            else:
                if move:
                    weeks = _phase.phase_week.filter(active=True, has_library=False).order_by('order')
                    for idy, _week in enumerate(weeks):
                        start = _week.starts + datetime.timedelta(weeks=1)
                        year, week, weekday = utils.get_year_and_week(start)
                        start, end = utils.get_start_end_dates(year, week)

                        _week.number_week = week
                        _week.starts = start
                        _week.ends = end
                        _week.order = idy + 1
                        _week.save()

        program.refresh_from_db()
        serializer = serializers.ProgramRetrieveSerializer(program, context={'request': request})
        return Response(serializer.data, status=200)


class CreateAndMoveWeeks(APIView):
    queryset = models.Week.objects.all()

    @transaction.atomic
    def post(self, request):
        data = request.data
        serializer = serializers.WeekPhaseSerializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        week = serializer.save()

        phase = week.phase
        program = phase.program

        phases = program.program_phase.filter(active=True).order_by('order')
        move = False
        for idx, _phase in enumerate(phases):
            if _phase.id == phase.id:
                move = True
            else:
                if move:
                    weeks = _phase.phase_week.filter(active=True).order_by('order')
                    for idy, _week in enumerate(weeks):
                        start = _week.starts + datetime.timedelta(weeks=1)
                        year, week, weekday = utils.get_year_and_week(start)
                        start, end = utils.get_start_end_dates(year, week)

                        _week.number_week = week
                        _week.starts = start
                        _week.ends = end
                        _week.order = idy + 1
                        _week.save()

        serializer = serializers.ProgramRetrieveSerializer(program, context={'request': request})
        return Response(serializer.data, status=200)


class DeleteAndMoveWeeks(APIView):
    queryset = models.Week.objects.all()

    @transaction.atomic
    def delete(self, request, pk):
        instance = get_object_or_404(models.Week, pk=pk)
        phase = instance.phase
        program = phase.program

        phases = program.program_phase.filter(active=True).order_by('order')
        move = False
        for idx, _phase in enumerate(phases):
            if _phase.phase_week.filter(id=instance.id).exists():
                weeks = _phase.phase_week.filter(active=True).order_by('order')
                for idy, _week in enumerate(weeks):
                    if _week.id == instance.id:
                        _week.delete()
                        move = True
                    else:
                        if move:
                            start = _week.starts - datetime.timedelta(weeks=1)
                            year, week, weekday = utils.get_year_and_week(start)
                            start, end = utils.get_start_end_dates(year, week)

                            _week.number_week = week
                            _week.starts = start
                            _week.ends = end
                            _week.order = _week.order - 1
                            _week.save()
            else:
                if move:
                    weeks = _phase.phase_week.filter(active=True).order_by('order')
                    for idy, _week in enumerate(weeks):
                        start = _week.starts - datetime.timedelta(weeks=1)
                        year, week, weekday = utils.get_year_and_week(start)
                        start, end = utils.get_start_end_dates(year, week)

                        _week.number_week = week
                        _week.starts = start
                        _week.ends = end
                        _week.order = idy + 1
                        _week.save()

        serializer = serializers.ProgramRetrieveSerializer(program, context={'request': request})
        return Response(serializer.data, status=200)


class DayWeekViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DayWeekSerializer
    queryset = models.Day.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend) 
    filterset_fields = ('day', 'week',)
    search_fields = ('day',)


class AllDaysWeeks(APIView):
    def get(self,request,phase):
        weeks = models.Week.objects.filter(phase=phase)
        serializer = serializers.AllDayWeekPhaseSerializer(weeks,many=True)
        return Response(serializer.data,status=200)


class ProgramPhaseDetail(APIView):
    def post(self,request):
        program = request.data.get('program')
        phase = request.data.get('phase')
        if program:
            program = get_object_or_404(models.Program, pk= int(program), active=True)
            serializer = serializers.ProgramDetaillSerializer(program)
            phases = models.Phase.objects.filter(program=program, active=True)
            serializer_program = serializers.PhaseDetailSerializer(phases,many=True)
            data = {
                'program' : serializer.data,
                'phases' : serializer_program.data
            }
            return Response(data,status=200)
        else:
            phase = get_object_or_404(models.Phase, pk= int(phase), active=True)
            serializer_program = serializers.PhaseDetailSerializer(phase)
            data = {
                'program' : None,
                'phases' : [serializer_program.data]
            }
            return Response(data,status=200)

class UserProgramView(APIView):
    def get(self,request,program):
        program = get_object_or_404(models.Program,pk=program) 
        users = program.athletes.all()
        serializer = serializers_user.TeamUserSerializer(users,many=True)
        return Response(serializer.data,status=200)


class ExerciseBlockDetailView(APIView):
    def get(self,request,exerciceblock):
        item = get_object_or_404(models.ExerciseBlock, pk=exerciceblock)
        serializer = serializers.ExerciseBlockDetailSerializer(item)
        return Response(serializer.data,status=200)

class BlockDetaillApp(APIView):
    def get(self,request,workout):
        items = models.Block.objects.filter(workout__id=workout,active=True)
        serializer = serializers.BlockTodaySerializerApp(items,many=True,context={'request': request})
        return Response(serializer.data,status=200)




class DayViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DaySerializer
    queryset = models.Day.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('day', 'date', 'week',)
    search_fields = ('day',)

    def get_serializer_class(self):
        if self.action == 'workouts':
            return serializers.WorkoutSerializer
        return self.serializer_class

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.active = False
        instance.save()

        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.day_as_library(instance)

        return Response(status=status.HTTP_201_CREATED)

    @action(["get"], detail=True)
    def workouts(self, request, pk=None):
        day = self.get_object()
        serializer = self.get_serializer(day.day_workout.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RowBlockTypeView(viewsets.ModelViewSet):
    serializer_class = serializers.RowBlockSerializer
    queryset = models.RowBlockType.objects.all()

class CategoryEquipmentView(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.CategoryEquipmentSerializer
    queryset = models.CategoryEquipment.objects.all()

class WorkoutViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkoutSerializer
    queryset = models.Workout.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('day','day__week__phase', 'start_time', 'end_time', 'active', 'has_library',)
    search_fields = ('name', 'location',)

    def get_serializer_class(self):
        if self.action == 'blocks':
            return serializers.BlockSerializer
        return self.serializer_class

    def perform_create(self,serializer):
        user = self.request.user
        item = serializer.save(
            institution=user.institution if user.institution else None
        )
        return item

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.workout_as_library(instance)

        return Response(status=status.HTTP_201_CREATED)

    @action(["get"], detail=True)
    def blocks(self, request, pk=None):
        workout = self.get_object()
        serializer = self.get_serializer(workout.block_workout.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlockTypeViewSet(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = serializers.BlockTypeSerializer
    queryset = models.BlockType.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('active',)
    search_fields = ('name',)


class BlockViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.BlockSerializer
    queryset = models.Block.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.BlockFilter
    search_fields = ('name', 'coding__name', 'sub_coding__name', 'type__name',)


    def get_serializer_class(self):
        if self.action == 'exercises':
            return serializers.ExerciseBlockSerializer
        return self.serializer_class

    def destroy(self, request, pk=None):
        instance = self.get_object()
        instance.active = False
        instance.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(["post"], detail=True)
    @transaction.atomic
    def library(self, request, pk=None):
        instance = self.get_object()
        tasks.block_as_library(instance)

        return Response(status=status.HTTP_201_CREATED)

    @action(["get"], detail=True)
    def exercises(self, request, pk=None):
        block = self.get_object()
        serializer = self.get_serializer(block.exercises.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CodingView(viewsets.ModelViewSet):
    pagination_class = None
    serializer_class = serializers.CodingSerializer
    queryset = models.Coding.objects.all()


class CodingCategoryView(viewsets.ModelViewSet):
    serializer_class = serializers.CodingCategorySerializer
    queryset = models.CodingCategory.objects.all()


class BlockExerciseCatalogView(viewsets.ReadOnlyModelViewSet):
    pagination_class = None
    serializer_class = serializers.BlockExerciseCatalogSerializer
    queryset = models.BlockExerciseCatalog.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('has_rest',)

class BlockExerciseCatalogSubparameterView(viewsets.ReadOnlyModelViewSet):
    serializer_class = serializers.BlockExerciseCatalogSubparameterSerializer
    queryset = models.BlockExerciseCatalogSubparameter.objects.all()
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filterset_fields = ('block_exercise_catalog',)

class ExerciseBlockRelatedCatalogView(viewsets.ModelViewSet):
    serializer_class = serializers.ExerciseBlockRelatedCatalogSerializer
    queryset = models.ExerciseBlockRelatedCatalog.objects.all()


    
    def perform_create(self,serializer):
        if serializer.is_valid():
            items = models.ExerciseBlockRelatedCatalog.objects.filter(
                exercise_block=serializer.validated_data['exercise_block'],
                ).exclude(
                    block_exercise_catalog_id__in=[15,16]
                )
            if len(items) > 2:
                if not serializer.validated_data['block_exercise_catalog'].has_rest:
                    raise exceptions.ValidationError(_('do you have a limit of items for block'))
        return serializer.save()


class ItemExerciseBlockRelatedCatalogView(viewsets.ModelViewSet):
    serializer_class = serializers.ItemExerciseBlockRelatedCatalogPanelSerializer
    queryset = models.ItemExerciseBlockRelatedCatalog.objects.all()
    


class LineExerciseBlockRelatedCatalogView(APIView):

    def delete(self, request, row, block):
        models.ItemExerciseBlockRelatedCatalog.objects.filter(
            row=row,
            catalog__exercise_block=block
        ).delete()
        models.RowBlockType.objects.filter(
            exercise_block=block,
            row=row
        ).delete()
        return Response(status=204)

class LineCloneExerciseBlockRelatedCatalogView(APIView):

    def get(self, request, row, block):
        items = models.ItemExerciseBlockRelatedCatalog.objects.filter(
            row=row,
            catalog__exercise_block=block
        )
        # last_row = models.ItemExerciseBlockRelatedCatalog.objects.filter(
        #     catalog__exercise_block=block
        # ).order_by('-row').first()
        if len(items) > 0:
            #  and last_row:
            row_it = models.RowBlockType.objects.filter(
                exercise_block=block,
                row=row
            ).first()
            if row_it:
                row_it = row_it.type
            else:
                row_it = 1
            utils.aument_lines(block, int(row) + 1)
            utils.aument_rows(block, int(row) + 1)
            utils.clone_line(items, int(row) + 1,row_it)
            items_n = models.ItemExerciseBlockRelatedCatalog.objects.filter(
                    row=int(row) + 1,
                    catalog__exercise_block=block
                )
            type = models.RowBlockType.objects.filter(row=int(row) + 1, exercise_block=block).first()
            serializer = serializers.ItemExerciseBlockRelatedCatalogPanelSerializer(items_n, many=True)
            serializer_type = serializers.RowBlockSerializer(type)
            data = {
                'values': serializer.data,
                'type': serializer_type.data
            }

            return Response(data,status=200)
        return Response({},status=200)

class WorkoutUserCalendarView(APIView):

    def get(self, request):
        number_weeks, date = utils.get_number_week(self.request.GET.get('date'))
        user = request.user
        workouts = []
        response = []

        items = utils.get_items_calendar(user,number_weeks,date)
        for item in items:
            if item.workout not in workouts:
                workouts.append(item.workout)
                serializer = serializers.WorkoutLibrarySerializer(item.workout)
                data = {
                    'workout':serializer.data,
                    'date': utils.get_date(item.workout)
                }
                response.append(data)

        return Response(response,status=201)

class TodayWorkoutUserCalendarView(APIView):

    def get(self, request):
        number_weeks, date, day = utils.get_number_week_current(self.request.GET.get('date'))
        user = request.user
        workouts = []
        response = []
        print(user)
        print(number_weeks)
        print(date.year)
        print(day)

        items = models.Block.objects.filter(
            athletes=user,
            workout__day__week__number_week__in=number_weeks,
            workout__day__week__starts__year=date.year,
            workout__day__day=day,
            workout__active=True
            )

        for item in items:
            if item.workout not in workouts:
                workouts.append(item.workout)
                serializer = serializers.WorkoutExersiceSerializer(item.workout,context={'request': request})
                response.append(serializer.data)

        return Response(response,status=200)



class ProgramLibraryViewSet(viewsets.ModelViewSet):
    queryset = models.Program.objects.all()
    serializer_class = serializers.ProgramLibrarySerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.ProgramLibraryFilter
    search_fields = ('name',)
    ordering_fields = ['name', 'created_at', 'updated_at']

    def get_queryset(self):
        return self.queryset.filter(active=True, has_library=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.ProgramLibraryInstanceSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        instance_serializer = serializers.ProgramLibraryInstanceSerializer(instance, context={'request': request})
        return Response(instance_serializer.data)

    def perform_create(self, serializer):
        instance = serializer.save()
        return instance

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True, context={'request': request})
        serializer.is_valid(raise_exception=True)
        instance = self.perform_update(serializer)
        instance_serializer = serializers.ProgramLibraryInstanceSerializer(instance, context={'request': request})
        return Response(instance_serializer.data)

    def perform_update(self, serializer):
        instance = serializer.save()
        return instance


class PhaseLibraryViewSet(viewsets.ModelViewSet):
    queryset = models.Phase.objects.all()
    serializer_class = serializers.PhaseLibrarySerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.PhaseLibraryFilter
    search_fields = ('name',)
    ordering_fields = ['name', 'created_at', 'updated_at']

    def get_queryset(self):
        return self.queryset.filter(active=True, has_library=True)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.PhaseLibraryInstanceSerializer
        return self.serializer_class


class WorkoutLibraryViewSet(viewsets.ModelViewSet):
    queryset = models.Workout.objects.filter(has_library=True)
    serializer_class = serializers.WorkoutLibrarySerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.WorkoutLibraryFilter
    search_fields = ('name', 'location',)
    ordering_fields = ['name', 'created_at', 'updated_at']


class BlockLibraryViewSet(viewsets.ModelViewSet):
    queryset = models.Block.objects.filter(has_library=True)
    serializer_class = serializers.BlockSerializer
    filter_backends = (df.OrderingFilter, df.SearchFilter, filters.DjangoFilterBackend)
    filter_class = filter_catalog.BlockFilter
    search_fields = ('name', 'coding__name', 'sub_coding__name', 'type__name',)
    ordering_fields = ['name', 'created_at', 'updated_at']


class PhaseLibraryImportAPIView(APIView):
    queryset = models.Program.objects.all()

    @transaction.atomic
    def post(self, request, program):
        body = request.data
        starts = datetime.datetime.strptime(body["starts"], '%Y-%m-%d')

        program = get_object_or_404(models.Program, id=program)
        phase_library = get_object_or_404(models.Phase, id=body["phase"])

        new_phase = copy.deepcopy(phase_library)
        new_phase.pk = None
        new_phase.has_library = False
        new_phase.save()

        start_import = starts
        end_import = None

        for i in phase_library.phase_week.filter(active=True, has_library=True).order_by('order'):
            year, week, weekday = utils.get_year_and_week(starts)
            start, end = utils.get_start_end_dates(year, week)

            kwargs = {
                'week': week,
                'start': start,
                'end': end
            }
            utils.import_week(request.user, i, new_phase, **kwargs)

            end_import = datetime.datetime.strptime(str(end), '%Y-%m-%d')

            nextDay = end + datetime.timedelta(days=1)
            starts = datetime.datetime.strptime(str(nextDay), '%Y-%m-%d')

        # Se crean workouts si el día importado no cuenta con alguno
        new_phase.refresh_from_db()
        for week in new_phase.phase_week.filter(active=True, has_library=False):
            for day in week.week_day.all().order_by('day'):
                if not day.day_workout.count():
                    workout = models.Workout.objects.create(name='Workout', day=day)
                    # utils.name_workout(workout)

        phases = program.program_phase.filter(active=True, has_library=False).order_by('order')

        imported = False
        last_order = 0

        if phases.count() > int(body["order"]):
            for idx, phase in enumerate(phases):
                if imported:
                    weeks = phase.phase_week.filter(active=True, has_library=False).order_by('order')
                    first_week = weeks.first()
                    if start_import.date() <= first_week.starts <= end_import.date():
                        start_week = end_import.date() + datetime.timedelta(days=1)
                        start_week = datetime.datetime.strptime(str(start_week), '%Y-%m-%d')

                        nextDay = None

                        for idy, _week in enumerate(weeks):
                            if not idy:
                                start_import = start_week

                            if nextDay:
                                days = abs(nextDay-_week.starts).days
                                # caculating the weeks, // = floor division operator
                                add = days // 7
                                start_week = start_week + datetime.timedelta(weeks=add)

                            year, week, weekday = utils.get_year_and_week(start_week)
                            start, end = utils.get_start_end_dates(year, week)

                            nextDay = _week.starts

                            _week.number_week = week
                            _week.starts = start
                            _week.ends = end
                            _week.order = idy + 1
                            _week.save()
                            end_import = datetime.datetime.strptime(str(end), '%Y-%m-%d')

                    phase.order = last_order + 1
                    phase.save()
                    last_order = phase.order

                if phase.order == int(body["order"]):
                    # Import
                    new_phase.program = program
                    new_phase.order = int(body["order"])
                    new_phase.save()

                    last_order = new_phase.order

                    imported = True
                    # Change order of the current item
                    weeks = phase.phase_week.filter(active=True, has_library=False).order_by('order')
                    first_week = weeks.first()
                    if start_import.date() <= first_week.starts <= end_import.date():
                        start_week = end_import.date() + datetime.timedelta(days=1)
                        start_week = datetime.datetime.strptime(str(start_week), '%Y-%m-%d')

                        nextDay = None

                        for idy, _week in enumerate(weeks):
                            if not idy:
                                start_import = start_week

                            if nextDay:
                                days = abs(nextDay-_week.starts).days
                                # caculating the weeks, // = floor division operator
                                add = days // 7
                                start_week = start_week + datetime.timedelta(weeks=add)

                            year, week, weekday = utils.get_year_and_week(start_week)
                            start, end = utils.get_start_end_dates(year, week)

                            nextDay = _week.starts

                            _week.number_week = week
                            _week.starts = start
                            _week.ends = end
                            _week.order = idy + 1
                            _week.save()
                            end_import = datetime.datetime.strptime(str(end), '%Y-%m-%d')

                    phase.order = last_order + 1
                    phase.save()
                    last_order = phase.order
        else:
            new_phase.program = program
            new_phase.order = int(body["order"])
            new_phase.save()


        serializer = serializers.ProgramRetrieveSerializer(program)
        return Response(serializer.data, status=200)


class WorkoutLibraryImportAPIView(APIView):
    queryset = models.Day.objects.all()

    @transaction.atomic
    def post(self, request, day):
        day = get_object_or_404(models.Day, id=day)
        workouts = models.Workout.objects.filter(id__in=request.data)

        for workout in workouts:
            utils.import_workout(request.user, workout, day)

        serializer = serializers.DayWeekSerializer(day)
        return Response(serializer.data, status=200)

class WorkoutCopyAPIView(APIView):
    queryset = models.Workout.objects.all()

    @transaction.atomic
    def post(self, request, workout):
        workout = get_object_or_404(models.Workout, id=workout)

        user = request.user
        data = request.data
        day = models.Day.objects.get(pk=data["day"])

        new_workout = copy.deepcopy(workout)
        new_workout.pk = None
        new_workout.day = day
        new_workout.created_by = user
        new_workout.updated_by = user
        new_workout.institution = user.institution
        new_workout.save()

        for i in workout.block_workout.filter(active=True, has_library=workout.has_library):
            utils.copy_block(user, i, new_workout)

        new_workout.refresh_from_db()
        serializer = serializers.WorkoutRetrieveSerializer(new_workout)
        return Response(serializer.data, status=status.HTTP_201_CREATED)