
from django.db import models

from uuid import uuid4
from django.db.models.deletion import SET_NULL
from django.utils.translation import ugettext as _





class Nivel(models.Model):    
    name = models.CharField(_("Nivel name"), max_length=50)    
   
    number_initial= models.IntegerField(_("First number"))
    
    number_next_level= models.IntegerField(_("Quantity next level"))
    
    description = models.CharField(_("Description"), max_length=500,default ="Description") 
        
    class Meta:
        verbose_name = "Nivel"
        verbose_name_plural = "Nivels"
                                  
    def __str__(self):
        """
        Returns a string representation of this `Nivel`.

        This string is used when a `Nivel` is printed in the console.
        """
        return "%s"%self.name
class NivelUser(models.Model):
    user = models.ForeignKey("security.User",
                            verbose_name=_("Related Users"),
                            on_delete= models.SET_NULL,
                            blank =True,
                            null=True)
    nivel = models.ForeignKey(Nivel,
                            verbose_name=_("Related Nivel"),
                            on_delete= models.SET_NULL,
                            blank =True,
                            null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by nivel"),
        on_delete=models.SET_NULL,
        related_name='nivel_updated_by_user',
        null=True,
        blank=True)
    quantity_trainings = models.IntegerField(_("quantity trainings"),blank=True,null=True) 
    class Meta:
        # unique_together = [['user',]]
        verbose_name = "Nivel User"
        verbose_name_plural = "Nivel Users"
                                  
    def __str__(self):
        """
        Returns a string representation of this `NivelUser`.

        This string is used when a `NivelUser` is printed in the console.
        """
        return "%s  %s" %(self.nivel ,self.user)   
class Block(models.Model):
    type_exercise = models.CharField(_("Type name"),max_length=50)
    catalog_block_type= models.ForeignKey("catalog.BlockType",
                                  verbose_name=_("BlockType nivel"),
                                  related_name= "catalog_block_type",
                                  on_delete=models.CASCADE,
                                  )
    
    
    class Meta:
        verbose_name = "Block"
        verbose_name_plural = "Blocks"
    
    def __str__(self):
        """
        Returns a string representation of this `Block`.

        This string is used when a `Block` is printed in the console.
        """
        return "%s"%self.type_exercise
class BlockNivel(models.Model):
    block = models.ForeignKey(Block, 
                                    verbose_name=_("block"),
                                    on_delete=models.CASCADE)
    nivel = models.ForeignKey(Nivel,verbose_name=_("nivel"),
                                    on_delete=models.CASCADE)
    
    class Meta:
        verbose_name = "Block nivel"
        verbose_name_plural = "Block nivels"
    
    def __str__(self):
        """
        Returns a string representation of this `BlockNivel`.

        This string is used when a `BlockNivel` is printed in the console.
        """
        return "%s" %(self.block)
    

    
class SetsReps(models.Model):
    block_nivel = models.ForeignKey(BlockNivel,
                                           verbose_name=_("Block Nivel setsreps") ,
                                           on_delete=models.CASCADE,
                                           related_name="block_nivel_setsreps"
                                           ) 
    
           
    
    sets = models.IntegerField(blank=True,null=True)
    
    reps_light_equip = models.CharField (_("reps light equipment"),
                                        max_length=300,
                                        blank=True,null=True) 
    
    reps_heavy_equip = models.CharField(_("reps heavy equipment"),
                                        max_length=300,blank=True,null=True)
    
    reps_lower_body_without_equipment = models.CharField(_("reps lower body"),
                                                            
                                        max_length=300,blank=True,null=True)
    reps_upper_body_without_equipment = models.CharField(_("reps upper body"),
                                        max_length=300,blank=True,null=True)
    
    intensity_equipment_RM = models.IntegerField(_("intensity"),blank=True,null=True)
    
    seconds_exercise = models.FloatField(_("seconds_exercise"),null=True, blank=True, default=None)
                        
    
    rest_exercise =  models.FloatField(_("rest exercise"),blank=True,null=True)
    
    rir = models.IntegerField(_("RIR"),blank=True,null=True)
    
    reps_vertical_jump=  models.IntegerField(_("reps vertical jump"),blank=True,null=True)

    reps_explosive = models.IntegerField(_("reps explosive"),blank=True,null=True)
    
    increment_load_week = models.IntegerField(_("increment load week"),blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True) 
    
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by setsreps"),
        on_delete=models.SET_NULL,
        related_name='setsreps_created_by_user',
        null=True,
        blank=True)
    
    updated_at = models.DateTimeField(auto_now=True)
    
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by setsreps"),
        on_delete=models.SET_NULL,
        related_name='setsreps_updated_by_user',
        null=True,
        blank=True)
    
    subparam = models.ForeignKey("catalog.BlockExerciseCatalogSubparameter",
                                on_delete=models.SET_NULL,
                                verbose_name =_("Related Subparameter"),
                                related_name = 'setsreps_subparameter',
                                null=True,
                                blank=True)
    class Meta:
        verbose_name_plural = "Sets and Reps"
        
    def __str__(self):
        """
        Returns a string representation of this `Sets and Reps`.

        This string is used when a `Sets and Reps` is printed in the console.
        """
        return "%s" %self.block_nivel
    
class HierarchyRegions(models.Model):
    name = models.CharField(_("Name Regiom"),max_length=30)
    region = models.ForeignKey("catalog.SubCategory",
                                  on_delete=models.CASCADE,
                                  verbose_name =_("Name Regions"),
                                  related_name = 'regions',
                                  null=True,
                                  blank=True,
                                  )
    class Meta:
        verbose_name = "Hierarchy Region"
        verbose_name_plural = "Hierarchy Regions"
        
    def __str__(self):
        """
        Returns a string representation of this `HierarchyRegions`.

        This string is used when a `HierarchyRegions` is printed in the console.
        """
        return "%s" %self.name


class WorkoutNivelPhase(models.Model):
    nivel = models.ForeignKey(NivelUser,
        verbose_name=_("Related Nivel"),
        on_delete=models.CASCADE,
        related_name='workout_user',
        null=True,
        blank=True)
    phase = models.DateTimeField(auto_now=True)
    
    accomplished = models.BooleanField(_('Realized WorkOut'), default=True)
    
    workout= models.JSONField()
    
    created_at = models.DateTimeField(auto_now_add=True) 
    
    class Meta:
        verbose_name = "Workout Nivel Phase"
        verbose_name_plural = "Workout Nivel Phases"
   
    def __str__(self):
        """
        Returns a string representation of this `WorkoutNivelPhase`.

        This string is used when a `WorkoutNivelPhase` is printed in the console.
        """
        return "%s" %(self.nivel)

class Category(models.Model):
    name = models.CharField(_("Name Category"),max_length=50)
    
    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
    def __str__(self):
        """
        Returns a string representation of this `Category`.

        This string is used when a `Category` is printed in the console.
        """
        return "%s" %(self.name)
class CategorySelection(models.Model):
    name = models.ForeignKey(Category,
                            verbose_name=_("Related category_selection"),
                            related_name="category_nivel",
                            blank=True,
                            null=True,
                            on_delete=SET_NULL)
   
    block_nivel = models.ForeignKey(
        BlockNivel,
        verbose_name=_("Related block_nivel"),
        on_delete=models.CASCADE)
    
    quantity_exercise = models.IntegerField(blank=True,null=True)
   
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by category_selection"),
        on_delete=models.SET_NULL,
        related_name='category_selection_created_by_user',
        null=True,
        blank=True,
        default=42)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by category_selection"),
        on_delete=models.SET_NULL,
        related_name='category_selection_updated_by_user',
        null=True,
        blank=True)
    
    class Meta:
        verbose_name = "Category selection"
        verbose_name_plural = "Categories selection"
                                  
    def __str__(self):
        """
        Returns a string representation of this `Category selection`.

        This string is used when a `Category selection` is printed in the console.
        """
        return "%s" %(self.name)
    
class CategorySelectionNivelUser(models.Model):
    category_selection = models.ForeignKey(Category,
                                           verbose_name=_("Related category_selection"),
                                           related_name="category_nivel_user",
                                           blank=True,
                                           null=True,
                                           on_delete=SET_NULL)
    nivel_user = models.ForeignKey(NivelUser,
                                           verbose_name=_("Related nivel_user"),
                                           related_name="nivel_user",
                                           blank=True,
                                           null=True,
                                           on_delete=SET_NULL)
    
    #equip = models.ForeignKey("catalog.SubCategory",
    #                                       verbose_name=_("Related equipment"),
    #                                       related_name="equip_user",
    #                                       blank=True,
    #                                       null=True,
    #                                       on_delete=SET_NULL
     #                        )
    active = models.BooleanField(_("Active category"), default=True)
    
    class Meta:
        verbose_name = "Category Selection Nivel User"
        verbose_name_plural = "Category Selection Nivel Users"
        
    def __str__(self):
        """
        Returns a string representation of this `CategorySelectionNivelUser`.

        This string is used when a `CategorySelectionNivelUser` is printed in the console.
        """
        return "%s" %(self.nivel_user)
    
    
    
    
class EquipUser(models.Model):
    equipment = models.ManyToManyField("catalog.SubCategory",
                                    verbose_name=_("Equipment"),
                                    related_name= "equip_user",
                                    
                                    blank=True,)
    
    user =  models.ForeignKey(
        "security.User",
        verbose_name=_("User Related"),
        on_delete=models.SET_NULL,
        related_name='equip_by_user',
        null=True,
        blank=True,
        )
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("created_by equip_user"),
        on_delete=models.SET_NULL,
        related_name='equip_user_created_by_user',
        null=True,
        blank=True,
        )
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("updated_by equip_user"),
        on_delete=models.SET_NULL,
        related_name='equip_user_updated_by_user',
        null=True,
        blank=True)
    class Meta:
        verbose_name = "Equipment User"
        verbose_name_plural = "Equipments Users"
        
    def __str__(self):
        """
        Returns a string representation of this `EquipUser`.

        This string is used when a `EquipUser` is printed in the console.
        """
        return "%s" %(self.user)