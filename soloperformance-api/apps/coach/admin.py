from django.contrib import admin
from . import models
# Register your models here.


    
    


@admin.register(models.Nivel)
class NivelAdmin(admin.ModelAdmin):
    list_display = ('name', 'number_initial','number_next_level')
    search_fields = ['name','number_initial','number_next_level']

@admin.register(models.NivelUser)
class NivelUser(admin.ModelAdmin):
    list_display = ('user','nivel' )
    search_fields = ['user','nivel','created_at',]
    
    
@admin.register(models.Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('type_exercise','catalog_block_type', )
    search_fields = ['catalog_block_type',]  
    
@admin.register(models.BlockNivel)
class BlockNivelAdmin(admin.ModelAdmin):
    list_display = ('block','nivel' )

    
    
@admin.register(models.CategorySelection)
class CategorySelectionAdmin(admin.ModelAdmin):
    list_display = ('name','block_nivel' ,'quantity_exercise')

@admin.register(models.SetsReps)
class SetsRepsAdmin(admin.ModelAdmin):
    list_display = ('block_nivel','sets' )
    search_fields = ['block_nivel',]
    
@admin.register(models.HierarchyRegions)
class HierarchyRegionsAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ['name',]
    
@admin.register(models.WorkoutNivelPhase)
class WorkoutNivelPhaseAdmin(admin.ModelAdmin):
    list_display = ('nivel','phase' ,'accomplished')
    

@admin.register(models.CategorySelectionNivelUser)
class CategorySelectionNivelUserAdmin(admin.ModelAdmin):
    list_display = ('category_selection','nivel_user' )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)   
    
    
@admin.register(models.EquipUser)
class EquipUserAmin(admin.ModelAdmin):
    list_display = ['user',]

    
    