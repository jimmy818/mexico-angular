from apps.coach import models as models_coach, utils, variation_horizontal
from apps.catalog import models as models_catalog
from apps.security import models as models_user
from apps.help_coach import utils as utils_help



def help_coach(user, equip_user=[]):
    exercises_equip  = utils.filter_equipment(equip_user)

   
    ##pera eliminar
    lower = models_catalog.SubCategory.objects.filter(category__in=models_catalog.Category.objects.filter(category_level= models_catalog.CategoryLevel.objects.get(name="Region"), code= "LOWER")).values("id")
    #hasta aquí
    region = [value["id"] for value in  lower]
  
    category_nivel_user_block = models_coach.CategorySelectionNivelUser.objects.filter(nivel_user= user).values("category_selection")
    category_selections=[]
    vertical_jump = False
    explosiveness = False
    # Select id of Category
    base = models_coach.Category.objects.filter(name= "Base").values("id").first()

    category_selections.append(base["id"])
    # See types categories 
    for options in category_nivel_user_block:
        category_selections.append(options["category_selection"])
        if int(options['category_selection'])== 7:
            vertical_jump = True
        elif int(options['category_selection'])== 8:
            explosiveness = True
            
    # Quantity of exercises and type
    exercise_type_quantity = models_coach.CategorySelection.objects.filter(name_id__in=category_selections,block_nivel__nivel= user.nivel).values("block_nivel",'quantity_exercise',"name")
    list_exercise=[]
    for value in exercise_type_quantity:
        if int(value['quantity_exercise']) >0 :
            list_exercise.append(value)
    # Regions primary and secundary
    regions = models_coach.HierarchyRegions.objects.all().values("name","region")
    regions_primary, regions_secundary , heavy_equip, light_equip= utils.hierarchy_regions_id(regions)

    type_exer = utils_help.exercises_types(exercises_do =list_exercise,
                            region =region,
                            regions_primary =regions_primary,
                            regions_secundary =regions_secundary,
                            heavy_equip= heavy_equip,
                            light_equip=light_equip,
                            user =user,
                            equip= equip_user,
                            exer_equip = exercises_equip,
                            explosive=explosiveness ,
                           vertical = vertical_jump)
    
    return type_exer
