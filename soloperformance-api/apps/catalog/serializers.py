from django.db import transaction
from django.shortcuts import get_object_or_404
from django.template.defaultfilters import pluralize
from django.utils.translation import ugettext as _
from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from . import fields, models, utils
from apps.security import models as model_user
from apps.teams import models as model_team
from apps.security import serializers as serializer_user
from apps.teams import serializers as serializer_team

import datetime


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Category
        fields = '__all__'
        read_only_fields = ['active']


class LevelCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CategoryLevel
        fields = '__all__'
        read_only_fields = ['active']

class MediaExerciceModelSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MediaExercice
        fields = '__all__'

class MediaExerciceSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.MediaExercice
        exclude = ('exercise',)


class SubCategorySerializer(serializers.ModelSerializer):
    level_category = CategorySerializer(many=True)
    class Meta:
        model = models.SubCategory
        fields = '__all__'
        read_only_fields = ['active']

class CustomSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SubCategory
        fields = ('id','name','image')

class ExcerciceSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Exercise
        fields = '__all__'
        read_only_fields = ['active']
    
    def get_media(self,instance):
        items = models.MediaExercice.objects.filter(exercise=instance.pk)
        serializer = MediaExerciceSerializer(items, many=True)
        return serializer.data

class ExcerciceMediaSerializer(serializers.ModelSerializer):
    media = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Exercise
        fields = ('id','english_name','spanish_name','media')
    
    def get_media(self,instance):
        items = models.MediaExercice.objects.filter(exercise=instance.pk)
        serializer = MediaExerciceSerializer(items, many=True)
        return serializer.data



class CurrentUserDefaultMixin(serializers.Serializer):

    def current_user_default(self):
        request = self.context["request"]
        user = request.user
        return user

    def create(self, validated_data):
        validated_data["created_by"] = self.current_user_default()
        validated_data["active"] = True
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.current_user_default()
        validated_data["active"] = True
        instance = super().update(instance, validated_data)
        return instance

class CurrentUserDefaultMixinNotActive(serializers.Serializer):

    def current_user_default(self):
        request = self.context["request"]
        user = request.user
        return user

    def create(self, validated_data):
        validated_data["created_by"] = self.current_user_default()
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.current_user_default()
        instance = super().update(instance, validated_data)
        return instance

class CurrentUserDefaultMixinHasLibrary(serializers.Serializer):

    def current_user_default(self):
        request = self.context["request"]
        user = request.user
        return user

    def create(self, validated_data):
        validated_data["created_by"] = self.current_user_default()
        validated_data["active"] = True
        validated_data["has_library"] = True
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.current_user_default()
        validated_data["has_library"] = True
        instance = super().update(instance, validated_data)
        return instance


class ProgramSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    team = fields.TeamField(required=False, allow_null=True)
    athletes = serializer_user.TeamUserSerializer(many=True, read_only=True)
    athletes_id = serializers.PrimaryKeyRelatedField(
        source='athletes',
        many=True,
        required=False,
        write_only=True,
        queryset=model_user.User.objects.all()
    )
    starts = serializers.SerializerMethodField(read_only=True) 
    ends = serializers.SerializerMethodField(read_only=True) 

    class Meta:
        model = models.Program
        fields = (
            'id',
            'name',
            'team',
            'athletes',
            'athletes_id',
            'starts',
            'ends',
        )

    def get_starts(self, instance):
        phase = instance.program_phase.filter(active=True).order_by('order').first()
        if phase:
            week = phase.phase_week.filter(active=True).order_by('order').first()
            if week and week.starts:
                return week.starts.strftime("%m-%d-%Y")
        return None

    def get_ends(self, instance):
        phase = instance.program_phase.filter(active=True).order_by('-order').first()
        if phase:
            week = phase.phase_week.filter(active=True).order_by('-order').first()
            if week and week.ends:
                return week.ends.strftime("%m-%d-%Y")
        return None


class ProgramPhasesSerializer(serializers.ModelSerializer):
    # Phases action from Program
    total = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Phase
        fields = (
            'id',
            'name',
            'order',
            'total',
        )

    def get_total(self, instance):
        volumen = utils.get_total_volumen(instance)
        return volumen if volumen else 0


""" list detail program """

class ProgramDetaillSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Program
        fields = (
            'id',
            'name'
        )


""" Start Custom Retrieve-Program """

class WorkoutRetrieveSerializer(serializers.ModelSerializer):
    # Workout for DqysRetrieve, only read only
    class Meta:
        model = models.Workout
        fields = (
            'id',
            'name',
            'start_time',
            'end_time',
            'location',
        )


class DqysRetrieveSerializer(serializers.ModelSerializer):
    # Dqys for WeeksRetrieve, only read only
    date = serializers.SerializerMethodField(read_only=True)
    workouts = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Day
        fields = (
            'id',
            'day',
            'date',
            'workouts',
        )

    def get_date(self, instance):
        if instance.week and instance.week.starts:
            year, week, weekday = utils.get_year_and_week(instance.week.starts)
            return datetime.date.fromisocalendar(year, week, instance.day).strftime("%m-%d-%Y")
        return None

    def get_workouts(self, instance):
        if instance.day_workout.count():
            workouts = instance.day_workout.filter(active=True).order_by('start_time')
            serializer = WorkoutRetrieveSerializer(workouts, many=True)
            return serializer.data
        return []


class WeeksRetrieveSerializer(serializers.ModelSerializer):
    # Weeks for PhasesRetrieve, only read only
    starts = serializers.DateField(format='%m-%d-%Y')
    ends = serializers.DateField(format='%m-%d-%Y')
    volumen = serializers.SerializerMethodField(read_only=True)
    days = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Week
        fields = (
            'id',
            'starts',
            'ends',
            'number_week',
            'volumen',
            'order',
            'days',
        )

    def get_volumen(self, instance):
        return instance.volumen if instance.volumen else 0

    def get_days(self, instance):
        if instance.week_day.count():
            days = instance.week_day.order_by('day')
            serializer = DqysRetrieveSerializer(days, many=True)
            return serializer.data
        return []


class PhasesRetrieveSerializer(ProgramPhasesSerializer):
    # Phases for ProgramRetrieve, only read only
    starts = serializers.SerializerMethodField(read_only=True)
    ends = serializers.SerializerMethodField(read_only=True)
    weeks = serializers.SerializerMethodField(read_only=True)

    def get_starts(self, instance):
        if instance.phase_week.count():
            week = instance.phase_week.filter(active=True).latest('-starts')
            if week and week.starts:
                return week.starts.strftime("%m-%d-%Y")
        return None

    def get_ends(self, instance):
        if instance.phase_week.count():
            week = instance.phase_week.filter(active=True).latest('ends')
            if week and week.ends:
                return week.ends.strftime("%m-%d-%Y")
        return None

    def get_weeks(self, instance):
        if instance.phase_week.count():
            weeks = instance.phase_week.filter(active=True).order_by('order')
            serializer = WeeksRetrieveSerializer(weeks, many=True)
            return serializer.data
        return []

    class Meta(ProgramPhasesSerializer.Meta):
        fields = ProgramPhasesSerializer.Meta.fields + ('starts','ends','weeks',)


class ProgramRetrieveSerializer(ProgramSerializer):
    # ProgramRetrieve for Retrieve Method
    phases = serializers.SerializerMethodField(read_only=True)

    def get_phases(self, instance):
        if instance.program_phase.count():
            phases = instance.program_phase.filter(active=True).order_by('order')
            serializer = PhasesRetrieveSerializer(phases, many=True)
            return serializer.data
        return []

    class Meta(ProgramSerializer.Meta):
        fields = ProgramSerializer.Meta.fields + ('phases',)

""" End Custom Retrieve-Program """


""" Start bulk Phase-Week-Day """

class PhaseWeekDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Day
        fields = (
            'id',
            'day',
            'week',
        )

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        validated_data["created_by"] = user

        instance = super().create(validated_data)
        workout = models.Workout.objects.create(
            name='Workout',
            day=instance,
            created_by=user)
        # utils.name_workout(workout)

        return instance


class PhaseWeekSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    name = serializers.CharField(default='Week', required=False)
    date = serializers.DateField(required=True, write_only=True)
    days = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = models.Week
        fields = (
            'id',
            'name',
            'phase',
            'date',
            'order',
            'days',
        )
        extra_kwargs = {
            'phase': { 'required': False },
            'order': { 'required': False },
        }

    @transaction.atomic
    def create(self, validated_data):
        phase = self.context['phase']
        date = validated_data.pop('date', None)
        days = validated_data.pop('days', [])

        year, week, weekday = utils.get_year_and_week(date)
        start, end = utils.get_start_end_dates(year, week)

        # validate_week = utils.validate_week_phase(phase, number_week)
        # if validate_week:
        #     raise exceptions.ValidationError(_('week is used in this phase'))

        validated_data['phase'] = phase
        validated_data['number_week'] = week
        validated_data['starts'] = start
        validated_data['ends'] = end

        instance = super().create(validated_data)
        if days:
            _days = []
            for i in days:
                _days.append({
                    'day': i,
                    'week': instance.id
                })
            print(_days)

            if _days:
                serializer = PhaseWeekDaySerializer(data=_days, many=True, context=self.context)
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance

class PhaseDetailSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):

    class Meta:
        model = models.Phase
        fields = (
            'id',
            'name'
        )
class PhaseSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    program = fields.ProgramField(required=True)
    order = serializers.IntegerField(required=True, write_only=True)
    weeks = PhaseWeekSerializer(many=True, write_only=True)

    class Meta:
        model = models.Phase
        fields = (
            'id',
            'name',
            'program',
            'order',
            'weeks',
        )

    @transaction.atomic
    def create(self, validated_data):
        weeks = validated_data.pop('weeks', [])

        program = validated_data.get('program')
        order = validated_data.get('order')
        reOrder = models.Phase.objects.filter(program=program, order=order).exists()

        instance = super().create(validated_data)

        if reOrder:
            phases = program.program_phase.filter(active=True).exclude(pk=instance.id).order_by('order')
            for idx, phase in enumerate(phases):
                if phase.order >= order:
                    phase.order = phase.order + 1
                    phase.save()

        if weeks:
            self.context["phase"] = instance
            for idx, week in enumerate(weeks):
                week["order"] = idx + 1
            serializer = PhaseWeekSerializer(data=weeks, many=True, context=self.context)
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return instance

""" End bulk Phase-Week-Day """


class WeekSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    phase = fields.PhaseField(required=True)
    created_by = serializer_user.InstitutionUserSerializer(read_only=True)
    updated_by = serializer_user.InstitutionUserSerializer(read_only=True)

    class Meta:
        model = models.Week
        fields = (
            'id',
            'name',
            'phase',
            'volumen',
            'order',
            'active',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
        )
        read_only_fields = ['active', 'created_by', 'updated_by']

class WeekPhaseSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    name = serializers.CharField(default='Week', write_only=True)
    date = serializers.DateField(required=True, write_only=True)
    volumen = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Week
        fields = '__all__'
        fields = (
            'id',
            'name',
            'date',
            'phase',
            'starts',
            'ends',
            'number_week',
            'volumen',
            'order',
        )
        read_only_fields = ('starts','ends',)
        extra_kwargs = {
            'order': { 'required': False },
        }

    def validate(self, attrs):
        date = attrs.pop("date", None)
        phase = attrs.get("phase", None)

        year, week, weekday = utils.get_year_and_week(date)
        start, end = utils.get_start_end_dates(year, week)
        attrs['number_week'] = week
        attrs['starts'] = start
        attrs['ends'] = end
        attrs["order"] = phase.phase_week.filter(active=True).count() + 1

        return attrs

    def get_volumen(self, instance):
        return instance.volumen if instance.volumen else 0

class DayWeekAllSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = ('id','day','week')


class AllDayWeekPhaseSerializer(serializers.ModelSerializer):
    days = serializers.SerializerMethodField(read_only=True) 
    class Meta:
        model = models.Week
        fields = ('id','name','order','days')

    def get_days(self,instance):
        days = models.Day.objects.filter(week=instance).order_by('day')
        serializer = DayWeekAllSerializer(days,many=True)
        return serializer.data



class DaySerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    week = fields.WeekField(required=True)
    created_by = serializer_user.InstitutionUserSerializer(read_only=True)
    updated_by = serializer_user.InstitutionUserSerializer(read_only=True)
    
    class Meta:
        model = models.Day
        fields = (
            'id',
            'day',
            'date',
            'week',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
        )
        read_only_fields = ['active', 'created_by', 'updated_by']

class DayWeekSerializer(CurrentUserDefaultMixinNotActive, serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = '__all__'

class WorkoutSerializer(serializers.ModelSerializer):
    day = fields.DayField(required=True)

    class Meta:
        model = models.Workout
        fields = (
            'id',
            'name',
            'day',
            'start_time',
            'end_time',
            'location',
            'active',
            'created_at',
            'updated_at',
            'has_library',
            'order'
        )
        read_only_fields = ['active','has_library',]

    # def validate(self, data):
    #     day = data.get('day', None)
    #     start_time = data.get('start_time', None)
    #     end_time = data.get('end_time', None)

    #     if not day and self.instance:
    #         day = self.instance.day

    #     query = day.day_workout.filter(start_time__lt=end_time).filter(end_time__gt=start_time)
    #     if self.instance:
    #         query = query.exclude(pk=self.instance.id)
    #     if query.exists():
    #         raise serializers.ValidationError(_('The assigned schedule is already occupied.'))

    #     return data

    def create(self, validated_data):
        instance = super().create(validated_data)
        # utils.name_workout(instance)
        # instance.refresh_from_db()
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        # utils.name_workout(instance)
        # instance.refresh_from_db()
        return instance


class BlockTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlockType
        fields = '__all__'

class CodingAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Coding
        fields = '__all__'

class SubCodingAppSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CodingCategory
        fields = '__all__'

class CodingSerializer(serializers.ModelSerializer):
    subcodings = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Coding
        fields = '__all__'
    
    def get_subcodings(self,instance):
        items = models.CodingCategory.objects.filter(coding=instance.id)
        serializer = CodingCategorySerializer(items,many=True)
        return serializer.data


class CodingCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.CodingCategory
        fields = '__all__'

class ExerciceBlockDefaultMixin(serializers.Serializer):

    def current_user_default(self):
        request = self.context["request"]
        user = request.user
        return user

    def institution_default(self):
        request = self.context["request"]
        user = request.user
        return user.institution

    def create(self, validated_data):
        validated_data["created_by"] = self.current_user_default()
        validated_data["institution"] = self.institution_default()
        validated_data["active"] = True
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        validated_data["updated_by"] = self.current_user_default()
        # validated_data["active"] = True
        instance = super().update(instance, validated_data)
        return instance

class ExerciceBlockSerializer(ExerciceBlockDefaultMixin,serializers.ModelSerializer):

    class Meta:
        model = models.ExerciseBlock
        fields = '__all__'

    def validate(self, attrs):
        block = attrs.get('block', None)
        if block and block.has_library:
            attrs["has_library"] = block.has_library

        return attrs

class ExerciseCustomNameSerializer(serializers.ModelSerializer):

    media = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Exercise
        fields = ('id','english_name','spanish_name','media','sub_category','institution','has_library','request_library')
    
    def get_media(self,instance):
        items = models.MediaExercice.objects.filter(exercise=instance.pk)
        serializer = MediaExerciceSerializer(items, many=True)
        return serializer.data

class ExerciseCustomAppNameSerializer(serializers.ModelSerializer):

    media = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Exercise
        fields = ('id','english_name','spanish_name','media')
    
    def get_media(self,instance):
        items = models.MediaExercice.objects.filter(exercise=instance.pk)
        serializer = MediaExerciceSerializer(items, many=True)
        return serializer.data

class ExerciceBlockMediaSerializer(ExerciceBlockDefaultMixin,serializers.ModelSerializer):
    exercise = ExerciseCustomNameSerializer()
    class Meta:
        model = models.ExerciseBlock
        fields = '__all__'


class ExerciceBlockDetailSerializer(ExerciceBlockDefaultMixin,serializers.ModelSerializer):

    class Meta:
        model = models.ExerciseBlock
        fields = '__all__'

class BlockSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    coding = fields.CodingField(required=True)
    sub_coding = fields.CodingCategoryField(required=False)
    type = fields.TypeField(required=True)
    workout = fields.WorkoutField(required=False)
    athletes = serializer_user.TeamUserSerializer(many=True, read_only=True)
    teams = serializer_team.TeamCustomSerializer(many=True, read_only=True)
    exerciseblock = serializers.SerializerMethodField(read_only=True)
    athletes_id = serializers.PrimaryKeyRelatedField(
        source='athletes',
        many=True,
        write_only=True,
        queryset=model_user.User.objects.all(),
        required=False
        
    )
    teams_id = serializers.PrimaryKeyRelatedField(
        source='teams',
        many=True,
        write_only=True,
        queryset=model_user.User.objects.all(),
        required=False
        
    )
    created_by = serializer_user.InstitutionUserSerializer(read_only=True)
    updated_by = serializer_user.InstitutionUserSerializer(read_only=True)
    has_library = serializers.BooleanField(initial=True, required=False)

    class Meta:
        model = models.Block
        fields = (
            'id',
            'name',
            'coding',
            'sub_coding',
            'type',
            'workout',
            'athletes',
            'athletes_id',
            'limit',
            'active',
            'teams_id',
            'teams',
            'created_at',
            'created_by',
            'updated_at',
            'updated_by',
            'has_library',
            'exerciseblock'
        )
        read_only_fields = ['active', 'created_by', 'updated_by']
    
    def validate(self, attrs):
        workout = attrs.get('workout', None)
        if workout:
            attrs["has_library"] = workout.has_library
        else:
            attrs["has_library"] = True

        return attrs

    def get_exerciseblock(self,instance):
        items = models.ExerciseBlock.objects.filter(block=instance)
        serializer = ExerciseBlockDetailSerializer(items,many=True)
        return serializer.data

class BlockTodaySerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):
    coding = CodingAppSerializer()
    sub_coding = SubCodingAppSerializer()
    exercises = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Block
        fields = (
            'id',
            'name',
            'coding',
            'sub_coding',
            'type',
            'limit',
            'active',
            'exercises'
        )
    def get_exercises(self,instance):
        items = models.ExerciseBlock.objects.filter(block=instance)
        serializer = ExerciseBlockAppDetailSerializer(items,many=True)
        return serializer.data
    
class BlockTodaySerializerApp(CurrentUserDefaultMixin, serializers.ModelSerializer):
    coding = CodingAppSerializer()
    sub_coding = SubCodingAppSerializer()
    exercises = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Block
        fields = (
            'id',
            'name',
            'coding',
            'sub_coding',
            'type',
            'limit',
            'active',
            'exercises'
        )
    def get_exercises(self,instance):
        items = models.ExerciseBlock.objects.filter(block=instance)
        serializer = ExerciseBlockDetailAppSerializer(items,many=True,context={'request': self.context.get('request')})
        return serializer.data



class ExerciseBlockSerializer(CurrentUserDefaultMixin, serializers.ModelSerializer):

    class Meta:
        model = models.ExerciseBlock
        fields = '__all__'
        read_only_fields = ['active']

class BlockExerciseCatalogSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlockExerciseCatalog
        fields = '__all__'

class BlockExerciseCatalogSubparameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.BlockExerciseCatalogSubparameter
        fields = '__all__'

class ExerciseBlockRelatedCatalogSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExerciseBlockRelatedCatalog
        fields = '__all__'

class CustomBlockExerciseCatalogSerializer(serializers.ModelSerializer):
    block_exercise_catalog = BlockExerciseCatalogSerializer()
    class Meta:
        model = models.ExerciseBlockRelatedCatalog
        fields = ('id','block_exercise_catalog')

class ItemExerciseBlockRelatedCatalogPanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemExerciseBlockRelatedCatalog
        fields = '__all__'

class ItemExerciseBlockRelatedCatalogSerializer(serializers.ModelSerializer):
    value1 = serializers.SerializerMethodField(read_only=True)
    value2 = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.ItemExerciseBlockRelatedCatalog
        fields = '__all__'

    
    def get_value1(self,instance):
        if instance.value1 != None and instance.value1 != '':
            request = self.context.get('request')
            user = request.user
            return utils.get_value1(instance, user)

        return 'lo que sea'
    
    def get_value2(self,instance):
        if instance.value2 != None and instance.value2 != '':
            request = self.context.get('request')
            user = request.user
            return utils.get_value2(instance, user)

        return None
    


class RowBlockSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RowBlockType
        fields = '__all__'

class CategoryEquipmentSerializer(serializers.ModelSerializer):
    equipment = CustomSubCategorySerializer(many=True)
    class Meta:
        model = models.CategoryEquipment
        fields = '__all__'

class ExerciseBlockDetailSerializer(serializers.ModelSerializer):
    exercise = ExerciseCustomNameSerializer()
    item_catalog_related = serializers.SerializerMethodField(read_only=True)
    values = serializers.SerializerMethodField(read_only=True)
    row_type = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.ExerciseBlock
        fields = ('id','exercise','comment','item_catalog_related','values','row_type')

    def get_item_catalog_related(self,instance):
        items = models.ExerciseBlockRelatedCatalog.objects.filter(exercise_block=instance)
        serializer = CustomBlockExerciseCatalogSerializer(items,many=True)
        return serializer.data

    def get_values(self,instance):
        items = models.ItemExerciseBlockRelatedCatalog.objects.filter(catalog__exercise_block=instance)
        serializer = ItemExerciseBlockRelatedCatalogPanelSerializer(items,many=True)
        return serializer.data

    def get_row_type(self,instance):
        items = models.RowBlockType.objects.filter(exercise_block=instance)
        serializer = RowBlockSerializer(items,many=True)
        return serializer.data

class ExerciseBlockAppDetailSerializer(serializers.ModelSerializer):
    exercise = ExerciseCustomAppNameSerializer()
    
    class Meta:
        model = models.ExerciseBlock
        fields = ('id','exercise')


class ExerciseBlockDetailAppSerializer(serializers.ModelSerializer):
    exercise = ExerciseCustomNameSerializer()
    item_catalog_related = serializers.SerializerMethodField(read_only=True)
    values = serializers.SerializerMethodField(read_only=True)
    row_type = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = models.ExerciseBlock
        fields = ('id','exercise','comment','item_catalog_related','values','row_type')

    def get_item_catalog_related(self,instance):
        items = models.ExerciseBlockRelatedCatalog.objects.filter(exercise_block=instance)
        serializer = CustomBlockExerciseCatalogSerializer(items,many=True)
        return serializer.data

    def get_values(self,instance):

        items = models.ItemExerciseBlockRelatedCatalog.objects.filter(catalog__exercise_block=instance)
        serializer = ItemExerciseBlockRelatedCatalogSerializer(items,many=True, context={'request': self.context.get('request')})
        return serializer.data

    def get_row_type(self,instance):
        items = models.RowBlockType.objects.filter(exercise_block=instance)
        serializer = RowBlockSerializer(items,many=True)
        return serializer.data


class ProgramLibrarySerializer(CurrentUserDefaultMixinHasLibrary, serializers.ModelSerializer):
    team = fields.TeamField(required=False, allow_null=True)
    athletes = serializer_user.TeamUserSerializer(many=True, read_only=True)
    athletes_id = serializers.PrimaryKeyRelatedField(
        source='athletes',
        many=True,
        required=False,
        write_only=True,
        queryset=model_user.User.objects.all()
    )
    duration = serializers.SerializerMethodField()
    days_per_week = serializers.SerializerMethodField()
    updated_by = serializer_user.InstitutionUserSerializer(read_only=True)

    class Meta:
        model = models.Program
        fields = (
            'id',
            'name',
            'team',
            'athletes',
            'athletes_id',
            'duration',
            'days_per_week',
            'updated_at',
            'updated_by',
        )

    def get_duration(self, instance):
        phases = instance.program_phase.filter(active=True).order_by('-created_at')
        if phases:
            week_count = 0
            for phase in phases:
                weeks = phase.phase_week.filter(active=True).order_by('-created_at')
                week_count += weeks.count()

            month = 4
            duration_months = week_count // month
            duration_weeks = week_count - (duration_months*month)

            if duration_months and duration_weeks:
                return '{month} Month{pmonth}, {week} Week{pweek}'.format(
                    month=duration_months,
                    pmonth=pluralize(duration_months, ',s'),
                    week=duration_weeks,
                    pweek=pluralize(duration_weeks, ',s')
                )
            if duration_months and not duration_weeks:
                return '{month} Month{pmonth}'.format(
                    month=duration_months,
                    pmonth=pluralize(duration_months, ',s')
                )
            if not duration_months and duration_weeks:
                return '{week} Week{pweek}'.format(
                    week=duration_weeks,
                    pweek=pluralize(duration_weeks, ',s')
                )

        return None

    def get_days_per_week(self, instance):
        phases = instance.program_phase.filter(active=True).order_by('-created_at')
        if phases:
            week_count = 0
            day_count = 0
            for phase in phases:
                weeks = phase.phase_week.filter(active=True).order_by('-created_at')
                week_count += weeks.count()
                for week in weeks:
                    day_count += week.week_day.count()

            if week_count and day_count:
                return day_count // week_count

        return None


class DayWeekLibrarySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Day
        fields = (
            'id',
            'day',
            'week',
        )
        extra_kwargs = {
            'week': { 'write_only': True }
        }

    @transaction.atomic
    def create(self, validated_data):
        request = self.context["request"]
        user = request.user
        validated_data["created_by"] = user

        instance = super().create(validated_data)
        workout = models.Workout.objects.create(
            name='Workout',
            day=instance,
            created_by=user)
        # utils.name_workout(workout)

        return instance


class WeekPhaseLibrarySerializer(CurrentUserDefaultMixinHasLibrary, serializers.ModelSerializer):
    name = serializers.CharField(default='Week library', required=False)
    days = serializers.ListField(child=serializers.IntegerField(), write_only=True)

    class Meta:
        model = models.Week
        fields = (
            'id',
            'name',
            'phase',
            'order',
            'days',
        )
        extra_kwargs = {
            'phase': { 'write_only': True },
            'order': { 'required': False }
        }

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        days = validated_data.pop('days', [])
        instance = super().create(validated_data)

        if days:
            data = []
            for i in days:
                data.append({
                    'day': i,
                    'week': instance.id
                })

            if data:
                serializer = DayWeekLibrarySerializer(data=data, many=True, context={'request': request})
                serializer.is_valid(raise_exception=True)
                serializer.save()

        return instance


class PhaseLibrarySerializer(CurrentUserDefaultMixinHasLibrary, serializers.ModelSerializer):
    updated_by = serializer_user.InstitutionUserSerializer(read_only=True)
    duration = serializers.SerializerMethodField(read_only=True)
    days_per_week = serializers.SerializerMethodField(read_only=True)
    weeks = WeekPhaseLibrarySerializer(many=True, write_only=True)

    class Meta:
        model = models.Phase
        fields = (
            'id',
            'name',
            'program',
            'duration',
            'days_per_week',
            'updated_at',
            'updated_by',
            'weeks',
        )
        # extra_kwargs = {
        #     'program': { 'required': True }
        # }

    def get_duration(self, instance):
        week_count = 0
        weeks = instance.phase_week.filter(active=True)
        if weeks:
            week_count += weeks.count()

            month = 4
            duration_months = week_count // month
            duration_weeks = week_count - (duration_months*month)

            if duration_months and duration_weeks:
                return '{month} Month{pmonth}, {week} Week{pweek}'.format(
                    month=duration_months,
                    pmonth=pluralize(duration_months, ',s'),
                    week=duration_weeks,
                    pweek=pluralize(duration_weeks, ',s')
                )
            if duration_months and not duration_weeks:
                return '{month} Month{pmonth}'.format(
                    month=duration_months,
                    pmonth=pluralize(duration_months, ',s')
                )
            if not duration_months and duration_weeks:
                return '{week} Week{pweek}'.format(
                    week=duration_weeks,
                    pweek=pluralize(duration_weeks, ',s')
                )

        return None

    def get_days_per_week(self, instance):
        week_count = 0
        day_count = 0

        weeks = instance.phase_week.filter(active=True)
        for week in weeks:
            week_count += 1
            day_count += week.week_day.count()

        if week_count and day_count:
            return day_count // week_count

        return None

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        weeks = validated_data.pop('weeks', [])

        instance = super().create(validated_data)

        if weeks:
            for idx, week in enumerate(weeks):
                week.update({
                    'phase': instance.id,
                    'order': idx + 1                    
                })

            serializer = WeekPhaseLibrarySerializer(data=weeks, many=True, context={'request': request})
            serializer.is_valid(raise_exception=True)
            serializer.save()

        return instance


class WeekPhaseLibraryInstanceSerializer(WeekPhaseLibrarySerializer):
    days = serializers.SerializerMethodField(read_only=True)

    def get_days(self, instance):
        if instance.week_day.count():
            days = instance.week_day.order_by('day')
            serializer = DayWeekLibrarySerializer(days, many=True)
            return serializer.data
        return []

    class Meta(WeekPhaseLibrarySerializer.Meta):
        fields = WeekPhaseLibrarySerializer.Meta.fields


class PhaseLibraryInstanceSerializer(PhaseLibrarySerializer):
    weeks = serializers.SerializerMethodField(read_only=True)

    def get_weeks(self, instance):
        if instance.phase_week.count():
            weeks = instance.phase_week.filter(active=True, has_library=True).order_by('order')
            serializer = WeekPhaseLibraryInstanceSerializer(weeks, many=True)
            return serializer.data
        return []

    class Meta(PhaseLibrarySerializer.Meta):
        fields = PhaseLibrarySerializer.Meta.fields + ('weeks',)


class ProgramLibraryInstanceSerializer(ProgramLibrarySerializer):
    phases = serializers.SerializerMethodField(read_only=True)

    def get_phases(self, instance):
        if instance.program_phase.count():
            phases = instance.program_phase.filter(active=True, has_library=True).order_by('order')
            serializer = PhaseLibraryInstanceSerializer(phases, many=True)
            return serializer.data
        return []

    class Meta(ProgramLibrarySerializer.Meta):
        fields = ProgramLibrarySerializer.Meta.fields + ('phases',)


class WorkoutBlockLibrarySerializer(CurrentUserDefaultMixinHasLibrary, serializers.ModelSerializer):
    coding = CodingAppSerializer(read_only=True)
    sub_coding = SubCodingAppSerializer(read_only=True)
    type = BlockTypeSerializer(read_only=True)
    # exercises = serializers.SerializerMethodField()

    class Meta:
        model = models.Block
        fields = (
            'id',
            'name',
            'coding',
            'sub_coding',
            'type',
            'workout',
            'limit',
            # 'exercises',
        )

    # def get_exercises(self, instance):
    #     return instance.exercises.filter(active=True, has_library=True).count()


class WorkoutLibrarySerializer(CurrentUserDefaultMixinHasLibrary, serializers.ModelSerializer):
    updated_by = serializer_user.InstitutionUserSerializer(read_only=True)
    blocks = serializers.SerializerMethodField(read_only=True)
    exercises = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = models.Workout
        fields = (
            'id',
            'name',
            'day',
            'updated_at',
            'updated_by',
            'institution',
            'blocks',
            'exercises',
            'has_library',
        )
        extra_kwargs = {
            'institution': { 'write_only': True },
            'has_library': { 'read_only': True }
        }

    def get_blocks(self, instance):
        blocks = instance.block_workout.filter(active=True, has_library=True).order_by('coding')
        if blocks:
            return BlockSerializer(blocks, many=True, context=self.context).data
        return []

    def get_exercises(self, instance):
        count = 0
        for block in instance.block_workout.filter(active=True, has_library=True):
            count += block.exercises.filter(active=True, has_library=True).count()
        return count


class WorkoutExersiceSerializer(CurrentUserDefaultMixinHasLibrary, serializers.ModelSerializer):
    media = serializers.SerializerMethodField(read_only=True)
    blocks = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = models.Workout
        fields = (
            'id',
            'name',
            'start_time',
            'end_time',
            'location',
            'media',
            'blocks'
        )
    
    def get_media(self,instance):
        item = models.ExerciseBlock.objects.filter(
            block__workout=instance
        ).first()
        if item:
            media = models.MediaExercice.objects.filter(exercise=item.exercise).first()
            if media:
                serializer = MediaExerciceSerializer(media)
                return serializer.data
        return None

    def get_blocks(self, instance):
        blocks = models.Block.objects.filter(
            workout=instance,
            active=True
        )
        if len(blocks) > 0:
            return BlockTodaySerializer(blocks,many=True,context=self.context).data
        return []

