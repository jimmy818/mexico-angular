from django.db import models
from django.utils.translation import ugettext as _
from django.db.models.deletion import SET_NULL


# Create your models here.
class VariationHorizontal(models.Model):
    name = models.CharField(_("Variation Horizontal"), max_length=100)

    change_exercises = models.BooleanField(verbose_name=_("Change Exercises"),default= True)
    change_reps      = models.BooleanField(verbose_name=_("Change Reps"),default= True)
    
    class Meta:
        verbose_name = "Variation Horizontal"
        verbose_name_plural= "Variations Horizontal"
        
    def __str__(self):
        """
        Returns a string representation of this `VariationHorizontal`.

        This string is used when a `VariationHorizontal` is printed in the console.
        """
        return "%s" %(self.name)

class VariationVertical(models.Model):
    name      = models.CharField(_("Variation Vertical"), max_length=100)
    intensity = models.IntegerField(_("intensity"),blank=True,null=True)
    volumen   = models.CharField(_("volumen"),
                                        max_length=300,blank=True,null=True)
    
    class Meta:
        verbose_name = " Variaton Vertical"
        verbose_name_plural= "Variations Vertical"
        
    def __str__(self):
        """
        Returns a string representation of this `VariationHorizontal`.

        This string is used when a `VariationHorizontal` is printed in the console.
        """
        return "%s" %(self.name)


class VariationVerticalProgram(models.Model):
    variation_vertical= models.ForeignKey(VariationVertical,
                                          verbose_name= _("Related Varition"),
                                          on_delete=models.SET_NULL,
                                          blank =True,
                                          null=True,default=1)
    
    phase = models.ForeignKey("catalog.Phase",
                                          verbose_name= _("Phase"),
                                          on_delete=models.SET_NULL,
                                          blank =True,
                                          null=True)
     
    class Meta:
        verbose_name = "Variation Vertical Phase"
        verbose_name_plural= "Variations Vertical Phase"
        
    def __str__(self):
        """
        Returns a string representation of this `VariationVerticalProgram`.

        This string is used when a `VariationVerticalProgram` is printed in the console.
        """
        return "%s" %(self.phase)
    
class WeekVariationHorizontal(models.Model):
    variation_horizontal= models.ForeignKey(VariationHorizontal,
                                          verbose_name= _(" Varition"),
                                          on_delete=models.SET_NULL,
                                          blank =True,
                                          null=True,
                                          default=1)
    week = models.ForeignKey("catalog.Week",
                                    verbose_name= _("Week"),
                                    on_delete=models.SET_NULL,
                                    blank =True,
                                    null=True)
    phase = models.ForeignKey("catalog.Phase",
                                          verbose_name= _("Phase"),
                                          related_name="Relation_phase",
                                          on_delete=models.SET_NULL,
                                          blank =True,
                                          null=True)
    
    class Meta:
        verbose_name = "Variation Horizontal Week"
        verbose_name_plural= "Variations Horizontal Weeks"
        
    def __str__(self):
        """
        Returns a string representation of this `WeekVariationHorizontal`.

        This string is used when a `WeekVariationHorizontal` is printed in the console.
        """
        return "%s" %(self.variation_horizontal)
    
    
class RegionsCategoryCoach(models.Model):
    
    category = models.ForeignKey("coach.CategorySelectionNivelUser",
                                 verbose_name=_("Related category_selection_nivel_user"),
                            related_name="nivel",
                            blank=True,
                            null=True,
                            on_delete=SET_NULL)
    regions = models.ManyToManyField("catalog.SubCategory",
                                           verbose_name=_("regions"),
                                           related_name="regions_category_coach",
                                           blank=True,
                                          
                             )
    phase = models.ForeignKey("catalog.phase",
                                verbose_name=_("Phase"),
                                related_name="phaseregionscategorycoach",
                                blank=True,
                                null=True,
                                on_delete=SET_NULL
                             )
                               
    class Meta:
        verbose_name = "Region Category"
        verbose_name_plural= "Regions Categories"
        
    def __str__(self):
        """
        Returns a string representation of this `RegionsCategoryCoach`.

        This string is used when a `RegionsCategoryCoach` is printed in the console.
        """
        return "%s" %(self.category) 
    
          
class ProgramWorkouts(models.Model):
    
    program = models.ForeignKey("catalog.Program",
                                          verbose_name= _("Program"),
                                          related_name="Relation_program",
                                          on_delete=models.SET_NULL,
                                          blank =True,
                                          null=True)  
    
    workouts_program = models.JSONField()

                               
    class Meta:
        verbose_name = "Program Workout"
        verbose_name_plural= "Program Workouts"
        
    def __str__(self):
        """
        Returns a string representation of this `ProgramWorkouts`.

        This string is used when a `ProgramWorkouts` is printed in the console.
        """
        return "%s" %(self.program)
from apps.help_coach import signals

    
    
