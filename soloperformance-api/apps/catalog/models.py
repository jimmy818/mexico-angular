from django.db import models
from django.db.models.fields import PositiveSmallIntegerField
from django.template.defaultfilters import default
from django.utils import tree
from django.utils.translation import ugettext as _
from uuid import uuid4
import os
import boto3
from common import enums

def path_and_rename(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'thumnails/'

    # return the whole path to the file
    return os.path.join(path, filename)

def path_and_rename_equipment(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'equipment/'

    # return the whole path to the file
    return os.path.join(path, filename)

def path_and_rename_icon(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'icons_category/'

    # return the whole path to the file
    return os.path.join(path, filename)

def path_and_rename_icon_exercie(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'icons_category_catalog/'

    # return the whole path to the file
    return os.path.join(path, filename)


class CategoryLevel(models.Model):
    name = models.CharField(_("Category name"), max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(_("category active"), default=True)

    class Meta:
        verbose_name = 'Category Level'
        verbose_name_plural = 'Categories Level'
    
    def __str__(self):
        """
        Returns a string representation of this `Category`.

        This string is used when a `Category` is printed in the console.
        """
        return "{}".format(self.name)

class Category(models.Model):
    name = models.CharField(_("Category name"), max_length=50)
    code = models.CharField(_("Code category"), max_length=150)
    category_level = models.ForeignKey(
        CategoryLevel, 
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(_("category active"), default=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        unique_together = [['code', 'category_level']]
    
    def __str__(self):
        """
        Returns a string representation of this `Category`.

        This string is used when a `Category` is printed in the console.
        """
        return "{}".format(self.name)


class SubCategory(models.Model):
    name = models.CharField(_("Subcategory name"), max_length=50)
    code = models.CharField(
        _("Code"), 
        max_length=50,
        unique=True)
    category = models.ForeignKey(
        'category', 
        verbose_name=_("Category"), 
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    level = models.PositiveSmallIntegerField(
        _("Level of subcategory"),
        null=True,
        blank=True)
    level_category = models.ManyToManyField(
        'category', 
        verbose_name=_("Category many level"), 
        related_name=_('category_many_level'),
        blank=True)
    image = models.ImageField(_("Image Equipment"), upload_to=path_and_rename_equipment,null=True,blank=True)    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(_("subcategory active"), default=True)

    class Meta:
        verbose_name = 'Subcategory'
        verbose_name_plural = 'Subcategories'
        
    
    def __str__(self):
        """
        Returns a string representation of this `SubCategory`.

        This string is used when a `SubCategory` is printed in the console.
        """
        return "{}".format(self.name)


class Exercise(models.Model):
    english_name = models.CharField(_("Name english"), max_length=250)
    identifier = models.CharField(_("Identifier"), max_length=250,null=True,blank=True)
    spanish_name = models.CharField(_("Name spanish"), max_length=250)
    sub_category = models.ManyToManyField(SubCategory, verbose_name=_("Subcategories Exercise"),blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("Created by"),
        on_delete=models.SET_NULL,
        related_name='exercise_updated_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(_("active"), default=True)
    has_library = models.BooleanField(_("has library"), default=False)
    note = models.TextField(_("Note of excercice"),null=True,blank=True)
    request_library = models.BooleanField(_("request active"), default=False)
     
    class Meta:
        verbose_name = 'Exercise'
        verbose_name_plural = 'Exercises'
        

    @property
    def institution(self):
        if self.created_by:
            if self.created_by.institution:
                return self.created_by.institution.id
        return None
    
    def __str__(self):
        """
        Returns a string representation of this `SubCategory`.

        This string is used when a `SubCategory` is printed in the console.
        """
        return "{}".format(self.english_name)

class CategoryEquipment(models.Model):
    name = models.CharField(_("Name Category"), max_length=50)
    equipment = models.ManyToManyField(SubCategory, verbose_name=_("Equipment related"))
    order = models.IntegerField(_("Ordering"),default=1)

    class Meta:
        ordering = ('order',)
        verbose_name = 'Category Equipment'
        verbose_name_plural = 'Categories Equipment'

class MediaExercice(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name=_("Related Exercice"), on_delete=models.CASCADE)
    path = models.TextField(_("Path s3 Exercice"))
    thumbnail = models.TextField(_("Path s3 thumbnail Exercice"),null=True,blank=True)

    class Meta:
        verbose_name = 'Media Exercice'
        verbose_name_plural = 'Media Exercices'
    
    def delete(self):
        print(self.path)
        if self.path:
            s3 = boto3.resource('s3')
            try:
                s3.Object('solo-performance-statics', self.path.split('net/')[1]).delete()
            except:
                pass
        super(MediaExercice, self).delete()

class GiftExercice(models.Model):
    exercise = models.ForeignKey(Exercise, verbose_name=_("Related Exercice"), on_delete=models.CASCADE)
    path = models.TextField(_("Path s3 Exercice"))

    class Meta:
        verbose_name = 'Gift Exercice'
        verbose_name_plural = 'Gift Exercices'
    
    def delete(self):
        print(self.path)
        if self.path:
            s3 = boto3.resource('s3')
            try:
                s3.Object('solo-performance-statics', self.path.split('net/')[1]).delete()
            except:
                pass
        super(MediaExercice, self).delete()

class Program(models.Model):
    """
    Description: Program Description
    """
    name = models.CharField(_("Program name"), max_length=250, blank=True, null=True)
    team = models.ForeignKey("teams.Team", verbose_name=_("Assigned team"), blank=True, null=True, on_delete=models.CASCADE)
    athletes = models.ManyToManyField( 
        "security.User",
        verbose_name=_("Assigned athletes"),
        blank=True)
    active = models.BooleanField(_("Program active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by program"),
        on_delete=models.SET_NULL,
        related_name='program_created_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by program"),
        on_delete=models.SET_NULL,
        related_name='program_updated_by_user',
        null=True,
        blank=True)
    has_library = models.BooleanField(_("library active"), default=False)

    class Meta:
        verbose_name = 'Program'
        verbose_name_plural = 'Programs'
        
    def __str__(self):
        """
        Returns a string representation of this `Program`.

        This string is used when a `Program` is printed in the console.
        """
        return "{}-{}".format(self.pk,self.name)


class Phase(models.Model):
    """
    Description: Phase Description
    """
    name = models.CharField(_("Phase name"), max_length=250)
    program = models.ForeignKey(
        Program,
        verbose_name=_("Program phase"),
        related_name='program_phase',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    order = models.PositiveSmallIntegerField(_("Order of phase"),default=1)
    active = models.BooleanField(_("Phase active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by phase"),
        on_delete=models.SET_NULL,
        related_name='phase_created_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by phase"),
        on_delete=models.SET_NULL,
        related_name='phase_updated_by_user',
        null=True,
        blank=True)
    has_library = models.BooleanField(_("library active"), default=False)

    class Meta:
        verbose_name = 'Phase'
        verbose_name_plural = 'Phases'
        
    def __str__(self):
        """
        Returns a string representation of this `Phase`.

        This string is used when a `Phase` is printed in the console.
        """
        return "{}-{}".format(self.pk,self.name)


class Week(models.Model):
    """
    Description: Week Description
    """
    name = models.CharField(_("Week name"), max_length=250)
    starts = models.DateField(_("week starts"), auto_now=False, auto_now_add=False, blank=True, null=True)
    ends = models.DateField(_("week ends"), auto_now=False, auto_now_add=False, blank=True, null=True)
    phase = models.ForeignKey(
        Phase,
        verbose_name=_("Phase week"),
        related_name='phase_week',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None)
    number_week = models.IntegerField(_("number week"),blank=True, null=True)
    volumen = models.IntegerField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(_("Order of week"))
    active = models.BooleanField(_("Week active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by week"),
        on_delete=models.SET_NULL,
        related_name='week_created_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by week"),
        on_delete=models.SET_NULL,
        related_name='week_updated_by_user',
        null=True,
        blank=True)
    has_library = models.BooleanField(_("has_library"), default=False)

    class Meta:
        verbose_name = 'Week'
        verbose_name_plural = 'Weeks'        
    
    def __str__(self):
        """
        Returns a string representation of this `Week`.

        This string is used when a `Week` is printed in the console.
        """
        return "{}-{}".format(self.pk,self.name)


class Day(models.Model):
    """
    Description: Day Description
    """
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7

    DAY_CHOICES = [
        (MONDAY, 'Monday'),
        (TUESDAY, 'Tuesday'),
        (WEDNESDAY, 'Wednesday'),
        (THURSDAY, 'Thursday'),
        (FRIDAY, 'Friday'),
        (SATURDAY, 'Saturday'),
        (SUNDAY, 'Sunday'),
    ]

    day = models.IntegerField(
        _("Day name"),
        choices=DAY_CHOICES,
        default=SUNDAY)
    week = models.ForeignKey(
        Week,
        verbose_name=_("Week day"),
        related_name='week_day',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by day"),
        on_delete=models.SET_NULL,
        related_name='day_created_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by day"),
        on_delete=models.SET_NULL,
        related_name='day_updated_by_user',
        null=True,
        blank=True)

    class Meta:
        verbose_name = 'Day'
        verbose_name_plural = 'Days'
        unique_together = ['day', 'week']

    def __str__(self):
        """
        Returns a string representation of this `Day`.

        This string is used when a `Day` is printed in the console.
        """
        return "{}-{}".format(self.pk,self.get_day_display())


class Workout(models.Model):
    """
    Description: Workout Description
    """
    name = models.CharField(_("Workout name"), max_length=250, blank=True, null=True)
    day = models.ForeignKey(
        Day,
        verbose_name=_("Day workout"),
        related_name='day_workout',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    start_time = models.TimeField(_("Start time"), blank=True, null=True)
    end_time = models.TimeField(_("End time"), blank=True, null=True)
    location = models.CharField(_("Workout location"), max_length=250, blank=True, null=True)
    active = models.BooleanField(_("Workout active"), default=True)
    order = models.PositiveSmallIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by workout"),
        on_delete=models.SET_NULL,
        related_name='workout_created_by_user',
        null=True,
        blank=True,
        default=None)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by workout"),
        on_delete=models.SET_NULL,
        related_name='workout_updated_by_user',
        null=True,
        blank=True,
        default=None)
    institution = models.ForeignKey(
        'teams.Institution', 
        verbose_name=_("institution created"), 
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    has_library = models.BooleanField(_("library active"), default=False)

    @property
    def program(self):
        try:
            program = self.day.week.phase.program
            return program
        except Exception as e:
            return None

    @property
    def team(self):
        try:
            program = self.day.week.phase.program
            return program.team
        except Exception as e:
            return None

    @property
    def athletes(self):
        try:
            program = self.day.week.phase.program
            return program.athletes.all()
        except Exception as e:
            return None

    class Meta:
        ordering = ['order',]
        verbose_name = 'Workout'
        verbose_name_plural = 'Workouts'        
    
    def __str__(self):
        """
        Returns a string representation of this `Workout`.

        This string is used when a `Workout` is printed in the console.
        """
        return "{}-{}".format(self.pk,self.name)


class BlockType(models.Model):
    """
    Description: BlockType Description
    """
    REGULAR = 'Regular'
    AMRAP = 'AMRAP'
    EMON = 'EMON'
    RFT = 'RFT'
    SUPERSET = 'SuperSet'

    name = models.CharField(_("Type name"), max_length=250)
    active = models.BooleanField(_("Type active"), default=True)

    class Meta:
        verbose_name = 'Block type'
        verbose_name_plural = 'Block types'
        
    def __str__(self):
        """
        Returns a string representation of this `Block`.

        This string is used when a `Block` is printed in the console.
        """
        return "{}".format(self.name)


class Block(models.Model):
    """
    Description: Block Description
    """
    name = models.CharField(_("Block name"), max_length=250, default="")
    coding = models.ForeignKey(
        'Coding',
        verbose_name=_("Coding block"),
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    sub_coding = models.ForeignKey(
        'CodingCategory',
        verbose_name=_("sub_coding category block"),
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    type = models.ForeignKey(
        BlockType,
        verbose_name=_("Type block"),
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    workout = models.ForeignKey(
        Workout,
        verbose_name=_("Block workout"),
        related_name='block_workout',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    athletes = models.ManyToManyField(
        "security.User",
        verbose_name=_("Assigned athletes"),
        blank=True)
    order = models.PositiveSmallIntegerField(default=1)
    limit = models.PositiveSmallIntegerField(_("Limit of exercises in a block"), blank=True, null=True)
    active = models.BooleanField(_("Block active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by block"),
        on_delete=models.SET_NULL,
        related_name='block_created_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by block"),
        on_delete=models.SET_NULL,
        related_name='block_updated_by_user',
        null=True,
        blank=True)
    has_library = models.BooleanField(_("library active"), default=False)

    class Meta:
        verbose_name = 'Block'
        verbose_name_plural = 'Blocks'        
    
    def __str__(self):
        """
        Returns a string representation of this `Block`.

        This string is used when a `Block` is printed in the console.
        """
        return "{}-{}".format(self.pk,self.type)


class ExerciseBlock(models.Model):
    """
    Description: ExerciseBlock  HERE START COPY
    """
    exercise = models.ForeignKey(
        Exercise, 
        verbose_name=_("Exercise"),
        on_delete=models.CASCADE)
    superset = models.ForeignKey(
        'ExerciseBlock', 
        verbose_name=_("Superset Exersice"),
        related_name='exerciseblock_superset',
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    code = models.CharField(_("Code block"), max_length=3,null=True,blank=True)
    block = models.ForeignKey(
        Block,
        verbose_name=_("Block exercise"),
        related_name='exercises',
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    comment = models.TextField(null=True,blank=True)
    active = models.BooleanField(_("Exercise block active"), default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("user created exercise block"),
        on_delete=models.SET_NULL,
        related_name='exerciseblock_created_by_user',
        null=True,
        blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("user update exercise block"),
        on_delete=models.SET_NULL,
        related_name='exerciseblock_updated_by_user',
        null=True,
        blank=True)
    institution = models.ForeignKey(
        "teams.Institution",
        verbose_name=_("Institution exercise block"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    has_library = models.BooleanField(_("has library"), default=False)

    class Meta:
        verbose_name = 'Exercise block'
        verbose_name_plural = 'Exercise blocks'

    def __str__(self):
        """
        Returns a string representation of this `Block`.

        This string is used when a `ExerciseBlock` is printed in the console.
        """
        return "{}".format(self.exercise.english_name)

class BlockExerciseCatalog(models.Model):
    title = models.CharField(_("Title"), max_length=50)
    icon_on = models.FileField(_("icon category"), upload_to=path_and_rename_icon_exercie, null=True,blank=True)
    icon_off = models.FileField(_("icon category"), upload_to=path_and_rename_icon_exercie, null=True,blank=True)
    order = models.IntegerField(_("Order"),default=1)
    has_rest = models.BooleanField(default=False)
    class Meta:
        ordering = ('order',)
        verbose_name = 'Block Exercise Catalog'
        verbose_name_plural = 'Block Exercise Catalogs'
    
    def __str__(self):
        return self.title

class RowBlockType(models.Model):
    TYPE = (
        (enums.TypeValueExersiceBlock.WARMUP.value, _('Warm Up')),
        (enums.TypeValueExersiceBlock.FAILURE.value, _('Failure')),
        (enums.TypeValueExersiceBlock.DROPSET.value, _('Drops set')),
        (enums.TypeValueExersiceBlock.DEFAULT.value, _('Default')),
    )
    exercise_block = models.ForeignKey(ExerciseBlock, on_delete=models.CASCADE)
    row = models.PositiveSmallIntegerField()
    type = models.PositiveSmallIntegerField(
        choices=TYPE,
        verbose_name=_('type'),
        default=enums.TypeValueExersiceBlock.WARMUP.value
    )

    class Meta:
        ordering = ('row',)
        verbose_name = 'Row Block Type'
        verbose_name_plural = 'Rows Block Type'
        unique_together = [['exercise_block', 'row']]

    
    # def __str__(self):
    #     return self.title

class ExerciseBlockRelatedCatalog(models.Model):
    exercise_block = models.ForeignKey(ExerciseBlock, on_delete=models.CASCADE)
    block_exercise_catalog = models.ForeignKey(BlockExerciseCatalog, on_delete=models.CASCADE)
    class Meta:
        ordering = ('block_exercise_catalog__id',)
        verbose_name = 'Exercise Block Related Catalog'
        verbose_name_plural = 'Exercise Block Related Catalogs'
        unique_together = [['exercise_block', 'block_exercise_catalog']]

class ItemExerciseBlockRelatedCatalog(models.Model):
    catalog = models.ForeignKey(ExerciseBlockRelatedCatalog, on_delete=models.CASCADE)
    catalog_subparameter = models.ForeignKey('BlockExerciseCatalogSubparameter', on_delete=models.CASCADE,blank=True,null=True)
    row = models.IntegerField()
    value1 = models.CharField(max_length=250)
    value2 = models.CharField(blank=True,null=True,max_length=250)
    value3= models.CharField(blank=True,null=True,max_length=250)
    value4 = models.CharField(blank=True,null=True,max_length=250)
    has_range = models.BooleanField(default=False)
    
    class Meta:
        ordering = ('row',)
        verbose_name = 'Item Exercise Block Related Catalog'
        verbose_name_plural = 'Items Exercise Block Related Catalog'
        unique_together = [['catalog', 'row']]
    

class BlockExerciseCatalogSubparameter(models.Model):
    TYPESUBPARAMETERS = (
        (enums.TypeSubparameters.NUM.value, _('Numeric')),
        (enums.TypeSubparameters.NUMERIC_CATALOG.value, _('Numeric Catalogs')),
        (enums.TypeSubparameters.PERCENTAGE_CATALOG.value, _('Percentage Catalogs')),
        (enums.TypeSubparameters.TIME.value, _('Time')),
        (enums.TypeSubparameters.CHOICE.value, _('Choice')),
        (enums.TypeSubparameters.PERCENTAGE.value, _('Percentaje')),
        (enums.TypeSubparameters.CHARACTER_OF_EFFORT.value, _('Character of effort')),
        (enums.TypeSubparameters.DECIMAL.value, _('Decimal')),
    )
    block_exercise_catalog = models.ForeignKey(BlockExerciseCatalog, on_delete=models.CASCADE)
    measure = models.CharField(_("Measure"), max_length=5,null=True,blank=True)
    title = models.CharField(_("Title"), max_length=50)
    type = models.IntegerField(
        choices=TYPESUBPARAMETERS,
        verbose_name=_('type'),
        default=enums.TypeSubparameters.NUM.value
    )
    order = models.IntegerField(_("ordering"),default=1)
    class Meta:
        ordering = ['type',]
        verbose_name = 'Block Exercise Catalog Subparameter'
        verbose_name_plural = 'Block Exercise Catalog Subparameters'
    
    def __str__(self):
        return self.title

class Coding(models.Model):
    name = models.CharField(_("name category"), max_length=50)
    icon = models.FileField(_("icon category"), upload_to=path_and_rename_icon)

    class Meta:
        verbose_name = 'Category Workout'
        verbose_name_plural = 'Categories Workouts'
    
    def __str__(self):
        return self.name
    

class CodingCategory(models.Model):
    name = models.CharField(_("name category"), max_length=50)
    coding = models.ForeignKey(Coding, verbose_name=_("item subcategory of category"), on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Coding Category'
        verbose_name_plural = 'Coding Categories'
    
    def __str__(self):
        return self.name