from django.contrib import admin
from . import models
from django.utils.translation import ugettext as _
# Register your models here.


class CategoryInline(admin.TabularInline):
    model = models.Category

class SubCategoryInline(admin.TabularInline):
    model = models.SubCategory

class BlockExerciseCatalogSubparameterInline(admin.TabularInline):
    model = models.BlockExerciseCatalogSubparameter

class BlockExerciseCatalogItemsInline(admin.TabularInline):
    model = models.ItemExerciseBlockRelatedCatalog

class MediaExersiceInLine(admin.TabularInline):
    model = models.MediaExercice

@admin.register(models.CategoryLevel)
class CategoryLevelAdmin(admin.ModelAdmin):
    list_display = ('name','active' )
    inlines = [
        CategoryInline,
        
    ]
    search_fields = ['name',]

@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','active' )
    inlines = [
        SubCategoryInline,
    ]
    search_fields = ['name',]

    
    
@admin.register(models.Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ('spanish_name',)
    list_filter = ('sub_category',)
    inlines = [
        MediaExersiceInLine
    ]
    search_fields = ['english_name','spanish_name']
    
    
@admin.register(models.Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('name','active' )
    search_fields = ['name',]


@admin.register(models.Phase)
class PhaseAdmin(admin.ModelAdmin):
    list_display = ('name','active' )
    search_fields = ['name',]


@admin.register(models.Week)
class WeekAdmin(admin.ModelAdmin):
    list_display = ('name','active' )
    search_fields = ['name',]


@admin.register(models.Day)
class DayAdmin(admin.ModelAdmin):
    list_display = ('day', )
    search_fields = ['day',]


@admin.register(models.Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ('name','active' )
    search_fields = ['name',]




@admin.register(models.Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('type','active' )
    search_fields = ['type',]

@admin.register(models.Coding)
class CodingAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name',]

@admin.register(models.CodingCategory)
class CodingCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name',]



@admin.register(models.BlockType)
class BlockTypeAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name',]

# @admin.register(models.MediaExercice)
# class MediaExerciceAdmin(admin.ModelAdmin):
#     list_display = ('path', )
#     search_fields = ['path',]

@admin.register(models.SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ['name',]

@admin.register(models.GiftExercice)
class GiftExerciceAdmin(admin.ModelAdmin):
    list_display = ('path', )
    search_fields = ['path',]

@admin.register(models.ExerciseBlock)
class ExerciseBlockAdmin(admin.ModelAdmin):
    list_display = ('exercise','has_library' )
    list_filter = ('has_library',)

    
@admin.register(models.BlockExerciseCatalog)
class BlockExerciseCatalogAdmin(admin.ModelAdmin):
    list_display = ('title', )
    inlines = [
        BlockExerciseCatalogSubparameterInline,
    ]


@admin.register(models.ExerciseBlockRelatedCatalog)
class ExerciseBlockRelatedCatalogAdmin(admin.ModelAdmin):
    list_display = ('exercise_block','block_exercise_catalog' )
    inlines = [
        BlockExerciseCatalogItemsInline,
    ]


@admin.register(models.CategoryEquipment)
class CategoryEquipmentAdmin(admin.ModelAdmin):
    list_display = ('name', )




    
    





