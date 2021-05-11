from django.contrib import admin
from django.db import models
from . import models

# Register your models here.
@admin.register(models.VariationHorizontal)
class VariationHorizontalAdmin(admin.ModelAdmin):
    list_display = ('name','change_exercises','change_reps' )



@admin.register(models.VariationVertical)
class VariationVerticalAdmin(admin.ModelAdmin):
    list_display = ('name','intensity','volumen' )



@admin.register(models.VariationVerticalProgram)
class VariationVerticalProgramAdmin(admin.ModelAdmin):
    list_display = ('variation_vertical','phase' )


@admin.register(models.WeekVariationHorizontal)
class WeekVariationHorizontalAdmin(admin.ModelAdmin):
    list_display = ('variation_horizontal','week' )
    
    
@admin.register(models.RegionsCategoryCoach)
class RegionsCategoryCoachAdmin(admin.ModelAdmin):
    list_display = ('category' ,"phase")
    
    
    
    
@admin.register(models.ProgramWorkouts)
class ProgramWorkoutsAdmin(admin.ModelAdmin):
    list_display = ('program' ,"workouts_program") 
