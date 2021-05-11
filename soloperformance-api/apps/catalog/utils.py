import datetime
import calendar
from isoweek import Week
import time
from datetime import date
from datetime import timedelta
from django.db.models import Sum
from django.template.defaultfilters import pluralize
from . import models
import copy
from apps.teams import models as team_model


def clone_line(items, row,r_type):
    for item in items:
        new_item = copy.deepcopy(item)
        new_item.pk = None
        new_item.row = row
        new_item.save()
        type = models.RowBlockType.objects.get_or_create(
            exercise_block=new_item.catalog.exercise_block,
            row=row,
            type=r_type
        )
    # return type

def aument_lines(block, row):
    items = models.ItemExerciseBlockRelatedCatalog.objects.filter(
            row__gte=row,
            catalog__exercise_block=block
        ).order_by('-row')
    for item in items:
        item.row = item.row + 1
        item.save()

def aument_rows(block, row):
    items = models.RowBlockType.objects.filter(
            row__gte=row,
            exercise_block=block
        ).order_by('-row')
    for item in items:
        item.row = item.row + 1
        item.save()
        

def add_data_categories(items):
    models.Category.objects.all().update(active=False)
    models.SubCategory.objects.all().update(active=False)
    models.CategoryLevel.objects.all().update(active=False)
    for item in items:
        category_level = create_category_level(item.get('catalog_dad'))
        category = create_category(item.get('category'),item.get('upper_category'),category_level)
        if category:
            category.active=True
            category.save()
            sub_categories = item.get('sub_categories',[])
            for sub_cat in sub_categories:
                get_or_create_sub_category(sub_cat,category)
    delete_category__sub_category_inactive()

def add_data_categories_custom(items):
    for item in items:
        category = create_category_custom(item.get('category'),item.get('upper_category'))
        if category:
            sub_categories = item.get('sub_categories',[])
            for sub_cat in sub_categories:
                get_or_create_sub_category(sub_cat,category)
        return category


def add_data_subcategories(items):
    print(items)
    for item in items:
        custom = add_data_categories_custom([item])
        dad = item.get('dad')
        if dad:
            sub = models.SubCategory.objects.filter(code=dad).first()
            if sub:
                sub.level_category.add(custom)
                sub.save()

def get_dad(col):
    if col <= 208:
        return 'OLY'
    if col <= 231:
        return 'PLY'
    if col <= 240:
        return 'SKL'

def get_new_cat_father(spred, value):
    item = spred.cell(rowx=0,colx=value).value
    # return 'hola'
    if len(item) > 0:
        return item
    else:
        return get_new_cat_father(spred, value - 1)

def get_or_add_excercice(item):
    excercice = models.Exercise.objects.filter(english_name=item).first()
    if excercice:
        return excercice
    else:
        item = models.Exercise.objects.create(
            english_name=item.replace("_", " "),
            spanish_name=item.replace("_", " "),
            identifier = item,
            has_library=True,
        )
        item.save()
        return item

def rename_exersice():
    excercice = models.Exercise.objects.all()
    for ex in excercice:
        ex.identifier = ex.english_name.replace(" ", "_")
        ex.english_name = ex.english_name.replace("_", " ")
        ex.spanish_name = ex.spanish_name.replace("_", " ")
        ex.save()

def add_sub_excercice(excercice,subcategory):
    subs = excercice.sub_category.all()
    sub = models.SubCategory.objects.filter(code=subcategory).first()
    if sub and sub not in subs:
        excercice.sub_category.add(sub)
        excercice.save()

def delete_category__sub_category_inactive():
    models.Category.objects.filter(active=False).delete()
    models.SubCategory.objects.filter(active=False).delete()
    models.CategoryLevel.objects.filter(active=False).delete()

    
def create_category(name, code, category_level):    
    if not name or not code:
        return None
    item = models.Category.objects.filter(code=code,category_level=category_level).first()
    if item:
        item.active = True
        item.save()
        return item
    else:
        try:
            item = models.Category.objects.create(
                name=name,
                code=code,
                category_level=category_level
            )
            item.save()
            return item
        except Exception as e:
            print(e)
            return None

def create_category_custom(name, code):    
    if not name or not code:
        return None
    item = models.Category.objects.filter(code=code,category_level__isnull=True).first()
    if item:
        item.active = True
        item.save()
        return item
    else:
        try:
            item = models.Category.objects.create(
                name=name,
                code=code
            )
            item.save()
            return item
        except Exception as e:
            print(e)
            return None

def create_category_level(name):
    if not name:
        return None
    item = models.CategoryLevel.objects.filter(name__iexact=name).first()
    # print(item)
    if item:
        item.active = True
        item.save()
        return item
    else:
        try:
            item = models.CategoryLevel.objects.create(
                name=name
            )
            item.save()
            return item
        except:
            return None

def get_or_create_sub_category(item=None,category=None):
    if not item or not category:
        return None
    name = item.get('name')
    code = item.get('code')
    
    if not name or not code:
        return None
    
    item = models.SubCategory.objects.filter(code=code,category=category).first()
    if item:
        item.active=True
        item.save()
        return item
    else:
        try:
            item = models.SubCategory.objects.create(
                name=name,
                code=code,
                category=category,
                level=0
            )
            item.save()
            return item
        except :
            return None


def validate_week_phase(phase,week):
    return models.Week.objects.filter(phase=phase,number_week=week,active=True).first()

def validate_week_name(phase,name):
    return models.Week.objects.filter(phase=phase,name__iexact=name,active=True).first()

def validate_week_phase_update(phase,week,pk):
    print(pk)
    return models.Week.objects.filter(phase=phase,number_week=week,active=True).exclude(pk=pk).first()

def validate_week_name_update(phase,name,pk):
    print(pk)
    return models.Week.objects.filter(phase=phase,name__iexact=name,active=True).exclude(pk=pk).first()

def get_total_volumen(phase):
    qs = phase.phase_week.filter(active=True).aggregate(total_volumen=Sum('volumen'))
    return qs["total_volumen"]

def start_end_days_of_week(p_year, p_week):
    firstdayofweek = datetime.datetime.strptime(f'{p_year}-W{int(p_week )- 1}-1', "%Y-W%W-%w").date()
    lastdayofweek = firstdayofweek + datetime.timedelta(days=6.9)
    return firstdayofweek, lastdayofweek

def get_year_and_week(date):
    # date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    year, week, weekday = date.isocalendar()
    return year, week, weekday

def get_start_end_dates(year, week):    
    d = date(year,1,1)
    if(d.weekday()<= 3):
        d = d - timedelta(d.weekday())
    else:
        d = d + timedelta(7-d.weekday())
    dlt = timedelta(days = (week-1)*7)
    return d + dlt,  d + dlt + timedelta(days=6)

def get_number_week(date):    
    weeks = []
    cal= calendar.Calendar()
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    for x in cal.itermonthdates(date.year,date.month):
        if x.isocalendar()[1] not in weeks:
            weeks.append(x.isocalendar()[1])
    return weeks, date

def get_number_week_current(date):    
    weeks = []
    cal= calendar.Calendar()
    date = datetime.datetime.strptime(date, '%Y-%m-%d')
    for x in cal.itermonthdates(date.year,date.month):
        if x.isocalendar()[1] not in weeks:
            weeks.append(x.isocalendar()[1])
    return weeks, date, calendar.weekday(date.year, date.month, date.day) + 1

def get_date(workout):
    week_numer = workout.day.week.number_week
    day = workout.day.day
    w = Week(workout.day.week.starts.year, week_numer)
    return get_day_date(w,day)

def get_day_date(w,day):
    if day == 1:
        return w.monday()
    if day == 2:
        return w.tuesday()
    if day == 3:
        return w.wednesday()
    if day == 4:
        return w.thursday()
    if day == 5:
        return w.friday()
    if day == 6:
        return w.saturday()
    if day == 7:
        return w.sunday()

def difference_between_times(start, end):
    start = datetime.datetime.combine(datetime.date.today(), start)
    end = datetime.datetime.combine(datetime.date.today(), end)
    difference = end - start
    total_seconds = difference.seconds

    min_segs = datetime.timedelta(minutes=1).seconds
    hour_mins = datetime.timedelta(hours=1).seconds // 60

    minutes = total_seconds // min_segs # minutes
    if minutes:
        seconds = total_seconds - (minutes*min_segs)
    hours = minutes // hour_mins
    if hours:
        minutes = minutes - (hours*hour_mins)
    if hours and minutes:
        return '{hour} Hour{phour} {minute} Minute{pminute}'.format(
                hour=hours,
                phour=pluralize(hours, ',s'),
                minute=minutes,
                pminute=pluralize(minutes, ',s')
            )
    if not hours and minutes:
        return '{minute} Minute{pminute}'.format(
                minute=minutes,
                pminute=pluralize(minutes, ',s')
            )
    if hours and not minutes:
        return '{hour} Hour{phour}'.format(
                hour=hours,
                phour=pluralize(hours, ',s')
            )
    if not hours and not minutes:
        return '{second} Second{psecond}'.format(
                second=total_seconds,
                psecond=pluralize(total_seconds, ',s')
            )
    return None




def get_value1(instance, user):
    if instance == '' and instance == None:
        return instance

    if instance.catalog_subparameter.title == '%BW':
        if float(user.weigth)> 0.0:
            return round((int(instance.value1) * float(user.weigth)) / 100 , 2)
        else:
            return instance.value1
    if instance.catalog_subparameter.title == '%Max':
        if float(user.FCM)> 0.0:
            return round((int(instance.value1) * float(user.FCM)) / 100 , 2)
        else:
            return instance.value1
    
    if instance.catalog_subparameter.title == 'zone':
        if float(user.FCM)> 0.0:
            if int(instance.value1) == 1:
                return '{} - {}'.format( round(((50 * float(user.FCM)) / 100) , 2), round(((60 * float(user.FCM)) / 100) , 2) )
            if int(instance.value1) == 2:
                return '{} - {}'.format( round(((60 * float(user.FCM)) / 100) , 2), round(((70 * float(user.FCM)) / 100) , 2) )
            if int(instance.value1) == 3:
                return '{} - {}'.format( round(((70 * float(user.FCM)) / 100) , 2), round(((80 * float(user.FCM)) / 100) , 2) )
            if int(instance.value1) == 4:
                return '{} - {}'.format( round(((80 * float(user.FCM)) / 100) , 2), round(((90 * float(user.FCM)) / 100) , 2) )
            if int(instance.value1) == 5:
                return '{} - {}'.format( round(((90 * float(user.FCM)) / 100) , 2), round(((100 * float(user.FCM)) / 100) , 2) )     
        else:
            return instance.value1
    if instance.catalog_subparameter.title == '%MAS':
        if float(user.MAS)> 0.0:
            return round((int(instance.value1) * float(user.MAS)) / 100 , 2)
        else:
            return instance.value1
    
    if instance.catalog_subparameter.title == '%MSS':
        if float(user.MSS)> 0.0:
            return round((int(instance.value1) * float(user.MSS)) / 100 , 2)
        else:
            return instance.value1
    return instance.value1

def get_value2(instance, user):
    if instance.catalog_subparameter.title == '%BW':
        if float(user.weigth)> 0.0:
            return round((int(instance.value2) * float(user.weigth)) / 100 , 2)
        else:
            return instance.value2
    if instance.catalog_subparameter.title == '%Max':
        if float(user.FCM)> 0.0:
            return round((int(instance.value2) * float(user.FCM)) / 100 , 2)
        else:
            return instance.value2
    
    if instance.catalog_subparameter.title == 'zone':
        if float(user.FCM)> 0.0:
            if int(instance.value2) == 1:
                return '{} - {}'.format( round(((50 * float(user.FCM)) / 100) , 2), round(((60 * float(user.FCM)) / 100) , 2) )
            if int(instance.value2) == 2:
                return '{} - {}'.format( round(((60 * float(user.FCM)) / 100) , 2), round(((70 * float(user.FCM)) / 100) , 2) )
            if int(instance.value2) == 3:
                return '{} - {}'.format( round(((70 * float(user.FCM)) / 100) , 2), round(((80 * float(user.FCM)) / 100) , 2) )
            if int(instance.value2) == 4:
                return '{} - {}'.format( round(((80 * float(user.FCM)) / 100) , 2), round(((90 * float(user.FCM)) / 100) , 2) )
            if int(instance.value2) == 5:
                return '{} - {}'.format( round(((90 * float(user.FCM)) / 100) , 2), round(((100 * float(user.FCM)) / 100) , 2) )     
        else:
            return instance.value2
    if instance.catalog_subparameter.title == '%MAS':
        if float(user.MAS)> 0.0:
            return round((int(instance.value2) * float(user.MAS)) / 100 , 2)
        else:
            return instance.value2
    
    if instance.catalog_subparameter.title == '%MSS':
        if float(user.MSS)> 0.0:
            return round((int(instance.value2) * float(user.MSS)) / 100 , 2)
        else:
            return instance.value2
    return instance.value2

def import_week(user, item, parent, **kwargs):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.phase = parent
    new_item.number_week = kwargs["week"]
    new_item.starts = kwargs["start"]
    new_item.ends = kwargs["end"]
    new_item.created_by = user
    new_item.updated_by = user
    new_item.has_library = False
    new_item.save()

    for i in item.week_day.all().order_by('day'):
        import_day(user, i, new_item)

def import_day(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.week = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.save()

    for i in item.day_workout.filter(active=True, has_library=True):
        import_workout(user, i, new_item)

def import_workout(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.day = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.institution = user.institution
    new_item.has_library = False
    new_item.save()

    for i in item.block_workout.filter(active=True, has_library=True):
        import_block(user, i, new_item)

def import_block(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.workout = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.has_library = False
    new_item.save()

    for i in item.exercises.filter(active=True, has_library=True):
        import_exerciseblock(user, i, new_item)

def import_exerciseblock(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.block = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.institution = user.institution
    new_item.has_library = False
    new_item.save()

    rows_blocktype = models.RowBlockType.objects.filter(exercise_block=item)
    for i in rows_blocktype:
        import_rowblocktype(i, new_item)

    exerciseblockrelated_catalogs = models.ExerciseBlockRelatedCatalog.objects.filter(exercise_block=item)
    for i in exerciseblockrelated_catalogs:
        import_exerciseblockrelatedcatalog(i, new_item)

def copy_day(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.week = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.save()

    for i in item.day_workout.filter(active=True, has_library=parent.has_library):
        copy_workout(user, i, new_item)

def copy_workout(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.day = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.institution = user.institution
    new_item.has_library = False
    new_item.save()

    for i in item.block_workout.filter(active=True, has_library=item.has_library):
        copy_block(user, i, new_item)

def copy_block(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.workout = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.save()

    for i in item.exercises.filter(active=True, has_library=item.has_library):
        copy_exerciseblock(user, i, new_item)

def copy_exerciseblock(user, item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.block = parent
    new_item.created_by = user
    new_item.updated_by = user
    new_item.institution = user.institution
    new_item.has_library = False
    new_item.save()

    rows_blocktype = models.RowBlockType.objects.filter(exercise_block=item)
    for i in rows_blocktype:
        import_rowblocktype(i, new_item)

    exerciseblockrelated_catalogs = models.ExerciseBlockRelatedCatalog.objects.filter(exercise_block=item)
    for i in exerciseblockrelated_catalogs:
        import_exerciseblockrelatedcatalog(i, new_item)

def import_rowblocktype(item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.exercise_block = parent
    new_item.save()

def import_exerciseblockrelatedcatalog(item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.exercise_block = parent
    new_item.save()

    items_exerciseblockrelatedcatalog = models.ItemExerciseBlockRelatedCatalog.objects.filter(catalog=item)
    for i in items_exerciseblockrelatedcatalog:
        import_itemexerciseblockrelatedcatalog(i, new_item)

def import_itemexerciseblockrelatedcatalog(item, parent):
    new_item = copy.deepcopy(item)
    new_item.pk = None
    new_item.catalog = parent
    new_item.save()

def name_workout(workout):
    day = workout.day
    if day:
        week = day.week
        if week:
            for idx, item in enumerate(week.week_day.all().order_by('day')):
                item.day_workout.filter(day=item, active=True).update(name='Day {}'.format(idx+1))



def get_items_calendar(user, number_weeks,date):
    # workouts atlhete
    if user.type == 4:
        return models.Block.objects.filter(
            athletes=user,
            workout__day__week__number_week__in=number_weeks,
            workout__day__week__starts__year=date.year,
            workout__active=True
            )
    # workouts coach
    if user.type == 3:
        teams = team_model.Team.objects.filter(coaches=user).values_list('pk',flat=True)
        return models.Block.objects.filter(
            workout__day__week__phase__program__teams__in=teams,
            workout__day__week__number_week__in=number_weeks,
            workout__day__week__starts__year=date.year,
            workout__active=True
            )
    # workouts institution
    if user.type == 3:
        return models.Block.objects.filter(
            athletes=user,
            workout__day__week__number_week__in=number_weeks,
            workout__day__week__starts__year=date.year,
            workout__active=True
            )
    return []