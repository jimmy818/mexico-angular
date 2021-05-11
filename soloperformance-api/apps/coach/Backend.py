import math
from operator import itemgetter
from . import utils
from apps.catalog.models import SubCategory, Exercise ,Category, CategoryLevel
from . import models
from . import variation_horizontal



## Training Upper and Lower
def training_total(user, equip_user =[],  uper="Upper", low="Lower"):

    workout_before = models.WorkoutNivelPhase.objects.filter(nivel  = user).values("id","phase",'accomplished',"workout")


    exercises_equip=[]
    exercises_equip  = utils.filter_equipment(equip_user)
    exer_before=[]
    increment = 0
    if len(workout_before) != 0:    
        increment, exer_before = variation_horizontal.increment_load_week_count_id_exercise(workout_before)

    equip_exercises = variation_horizontal.pop_exercise_variation_hotizontal_unequal(exercises_equip, exer_before)
    if 0 >= int(increment) <=5:
        variation = increment
    else:
        variation = 0
    

    # Take id for nivel_block 
    category_nivel_user_block = models.CategorySelectionNivelUser.objects.filter(nivel_user= user)
    category_selections=[]
    vertical_jump = False
    explosiveness = False
    # Select id of Category 
    category_selections=[]
    base = models.Category.objects.filter(name= "Base").values("id").first()
    category_selections.append(base["id"])
    for options in category_nivel_user_block:
        if options.category_selection:
            category_selections.append(options.category_selection.id)
        if options.category_selection:
            vertical_jump = True
        elif str(options.category_selection)   == str("Explosiveness"):
            explosiveness = True

    myo = models.BlockNivel.objects.filter(block__type_exercise="Myofascial").filter(nivel=user.nivel).values("id").first()
    mob = models.BlockNivel.objects.filter(block__type_exercise="Mobility").filter(nivel=user.nivel).values("id").first()
    skil = models.BlockNivel.objects.filter(block__type_exercise="Skills").filter(nivel=user.nivel).values("id").first()
    plyo = models.BlockNivel.objects.filter(block__type_exercise="Plyo").filter(nivel=user.nivel).values("id").first()
    streng_primary = models.BlockNivel.objects.filter(block__type_exercise="Primary Strength").filter(nivel=user.nivel).values("id").first()
    streng_secundary = models.BlockNivel.objects.filter(block__type_exercise="Secondary Strength").filter(nivel=user.nivel).values("id").first()
    esd = models.BlockNivel.objects.filter(block__type_exercise="Esd").filter(nivel=user.nivel).values("id").first()
    recovery = models.BlockNivel.objects.filter(block__type_exercise="Recovery").filter(nivel=user.nivel).values("id").first()
    activation = models.BlockNivel.objects.filter(block__type_exercise="Activation").filter(nivel=user.nivel).values("id").first()

    
    # Quantity of exercises and type

    exercise_type_quantity = models.CategorySelection.objects.filter(name_id__in=category_selections,block_nivel__nivel= user.nivel).values("block_nivel",'quantity_exercise')
    number_exercises = utils.sum_exercise_block_nivel(exercise_type_quantity)  



# Regions primary and secundary
    regions = models.HierarchyRegions.objects.all().values("name","region")
    regions_primary, regions_secundary , heavy_equip, light_equip= utils.hierarchy_regions_id(regions)

    

    
    # Exercises Miofascial
    miofascial_upper_aleatory=[]
    miofascial_upper= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = uper).filter(sub_category__code="MYO").values("id"), equip_exercises)

    if miofascial_upper:
        miofascial_upper_aleatory= utils.random_exercises(miofascial_upper, math.ceil(number_exercises[myo["id"]]/2))
        
    # Exer mobility
    mobility_upper= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = uper).filter(sub_category__code="MOB").values("id"), equip_exercises)
    mobility_upper_aleatory= utils.random_exercises(mobility_upper, math.ceil(number_exercises[mob["id"]]/2))

    # Exer Skills
    skills_upper=[]
    skills_upper= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = uper).filter(sub_category__code="SKL").values("id"), equip_exercises)

    skills_upper_aleatory=[]
    if skills_upper:
        skills_upper_aleatory= utils.random_exercises(skills_upper, math.ceil(number_exercises[skil["id"]]/2))

    #Exer Plyo 
    plyo_upper =[]
    plyo_upper_aleatory=[]
    plyo_upper= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = uper).filter(sub_category__code="PLY").values("id"), equip_exercises)


    if plyo_upper and len(plyo_upper) >= int(number_exercises[plyo["id"]])  :
        plyo_upper_aleatory= utils.random_exercises(plyo_upper, math.ceil(number_exercises[plyo["id"]]/2))
    else:
        plyo_upper_aleatory= utils.random_exercises(plyo_upper, math.ceil( len(plyo_upper)/2))
                

    # Exer Core  is --- activation ---      
    core_upper= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = uper).filter(sub_category__code="CORE").values("id"), equip_exercises)

    core_upper_aleatory= utils.random_exercises(core_upper, math.ceil(number_exercises[activation["id"]]/2))
    
    # Exer Strenght Primary lower
    exercises_strenght_primary= Exercise.objects.filter(sub_category__in=regions_primary).filter(sub_category__code="STR").values("id")
    strenght_primary_aleatory= utils.random_exercises(exercises_strenght_primary,math.ceil(number_exercises[streng_primary["id"]]))
    
    # Exer Strenght Secundary lower
    exercises_strenght_secundary= Exercise.objects.filter(sub_category__in=regions_secundary).filter(sub_category__code="STR").values("id")

    strenght_secundary_aleatory= utils.random_exercises(exercises_strenght_secundary,math.ceil(number_exercises[streng_secundary["id"]]))       

    # Extract the id of all LOWER zones

    # Exer mobility     
    mobility_lower= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = low).filter(sub_category__code="MOB").values("id"), equip_exercises)   
    mobility_lower_aleatory= utils.random_exercises(mobility_lower, math.ceil(number_exercises[mob["id"]]/2))

    # Exer Skills
    skills_lower=[]
    skills_lower_aleatory=[]
    skills_lower= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = low).filter(sub_category__code="SKL").values("id"), equip_exercises)


    
    if skills_lower:
        skills_lower_aleatory= utils.random_exercises(skills_lower, math.ceil(number_exercises[skil["id"]]/2))

    # Exer Core  ---activation---
    core_lower= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = low).filter(sub_category__code="CORE").values("id"), equip_exercises)

    core_lower_aleatory= utils.random_exercises(core_lower, math.ceil(number_exercises[activation["id"]]/2))

    # Exercises Miofascial
    miofascial_lower_aleatory=[]
    miofascial_lower= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = low).filter(sub_category__code="MYO").values("id"), equip_exercises)

    if miofascial_lower and len(miofascial_lower) >= int(math.ceil(number_exercises[myo["id"]]/2)):
        miofascial_lower_aleatory= utils.random_exercises(miofascial_lower, math.ceil(number_exercises[myo["id"]]/2))
    else:
        miofascial_lower_aleatory= utils.random_exercises(miofascial_lower,  math.ceil(len(miofascial_lower)/2))


    #Exer Plyo lower
    plyo_lower =[]
    plyo_lower_aleatory=[]
    plyo_lower = utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name=low).filter(sub_category__code="MYO").values("id"), equip_exercises)
    
    if plyo_lower and len(plyo_lower) >= int(number_exercises[plyo["id"]])  :
        plyo_lower_aleatory= utils.random_exercises(plyo_lower, math.ceil(number_exercises[plyo["id"]]/2))
    else:
        plyo_lower_aleatory= utils.random_exercises(plyo_lower, math.ceil(len(plyo_lower)/2))    
        
        # Select region body for the exercises         
    if len(plyo_upper_aleatory) >= 1 and len(plyo_lower_aleatory) >=1:
        war_body = utils.zone_body(strenght_primary_aleatory+ strenght_secundary_aleatory  + core_upper_aleatory +core_lower_aleatory+ skills_upper_aleatory + skills_lower_aleatory+ mobility_upper_aleatory + miofascial_upper_aleatory + plyo_upper_aleatory)
    else:
        war_body = utils.zone_body(strenght_primary_aleatory+  strenght_secundary_aleatory + core_upper_aleatory + skills_upper_aleatory + skills_lower_aleatory+ mobility_upper_aleatory + miofascial_upper_aleatory + miofascial_lower_aleatory +core_lower_aleatory)
    
    # Exer ESD      
    exercises_esd = Exercise.objects.filter (sub_category__code = "ESD").values("id")
    exercises_esd_aleatory = utils.random_exercises ( exercises_esd ,number_exercises[esd["id"]])

    # sorted for body more use 
    war_body_sorted = dict(sorted(war_body.items(), key=itemgetter(1),reverse=True))     

        # Exer stretching -- RECOVERY --
    #exercises_stretching = utils.stt_ejercicios(war_body_sorted)
    exercises_stretching= Exercise.objects.filter(sub_category__in=list(war_body_sorted)[:number_exercises[recovery["id"]]]).filter(sub_category__code="STT").values("id")     
    exercises_stretching_aleatory = utils.random_exercises(exercises_stretching , math.ceil(number_exercises[recovery["id"]]))

    results = utils.result(  mobility           = (mobility_lower_aleatory + mobility_upper_aleatory),
                                activation         = (core_lower_aleatory + core_upper_aleatory),
                                skills             = (skills_lower_aleatory + skills_upper_aleatory),
                                strenght_primary   = strenght_primary_aleatory,
                                strenght_secundary = strenght_secundary_aleatory ,
                                esd                = exercises_esd_aleatory,
                                stretching         = exercises_stretching_aleatory,
                                myofascial         = (miofascial_upper_aleatory + miofascial_lower_aleatory),
                                plyo               = (plyo_lower_aleatory + plyo_upper_aleatory)
                            )
    
    
    
    sets_reps = models.SetsReps.objects.filter(block_nivel__in= set(list(number_exercises.keys())))

    result_set_reps = utils.reps_sets(  values=sets_reps,
                                        exercise =results,
                                        user=user,
                                        variation= variation,
                                        heavy_equip=heavy_equip,
                                        light_equip=light_equip,
                                        equip= equip_user,
                                        vertical = vertical_jump,
                                        explosive = explosiveness,
                                        )
    return result_set_reps