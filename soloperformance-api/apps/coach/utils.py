from apps.catalog.models import Exercise
from apps.coach import variation_horizontal
from itertools import chain
from apps.catalog.models import SubCategory, Exercise ,Category, CategoryLevel
import random
from . import models
from apps.catalog import models as models_catalog
from common import enums
from collections import defaultdict
from apps.security import models as models_user



#select number exercise for nivel_block
def sum_exercise_block_nivel(exercise):
    dicionario= {}
    keys = [key['block_nivel'] for key in exercise ]    
    values = [value['quantity_exercise'] for value in exercise]    
    for key,value in zip(keys,values):
        if key not in dicionario.keys():
            dicionario[key] = value
       
        else:
            dicionario[key] =((dicionario[key])+ value)       
         
    for key , value in list(dicionario.items()):
        if value < 0:      
            dicionario[key] =0
    return dicionario
# Filter equipment
# Filter equipment

def filter_equipment(equipments=[]):
    
    exercises=[]
    # if not equipment
    exercise = Exercise.objects.exclude(sub_category__category__code="EQUIPMENT").values("id")

    exercises.append(exercise)
        
    exercise_equip = Exercise.objects.filter(sub_category__in= SubCategory.objects.filter(pk__in=equipments)).values("id")
    result = list(chain(exercise,exercise_equip))
    return result


# Random exercises
def random_exercises(datas, number=1):
   
    data =[dato for dato in datas]
    selects = random.sample(list(data),int(number))
    result = [select for select in selects]
    return result

# Id seccion regions or heavy and light equipment
def hierarchy_regions_id(hierarchy_regions):
    primary_region=[]
    secundary_region=[]
    heavy_equip = []
    light_equip  =[]
    for name in hierarchy_regions:
        if str(name['name']) == "Primary":
            primary_region.append(name['region'])
        elif str(name['name']) == "Secundary":
            secundary_region.append(name['region'])
        elif str(name['name']) == 'Light equip':
            light_equip.append(name['region'])
        elif str(name['name']) == 'Heavy equip':
            heavy_equip.append(name['region'])    
    return primary_region,secundary_region, heavy_equip, light_equip

# Selec nivel for days workout        
def updated_nivel(nivel_user):
    niveles = models.Nivel.objects.all()
    if nivel_user.quantity_trainings == 0:
        number_trainings = int(enums.NivelsQuantityExercise[nivel_user.nivel.name].value)
        models.NivelUser.objects.filter(pk=nivel_user.id).update(quantity_trainings=number_trainings)
        
    for nivel in niveles:   
        if int(nivel_user.quantity_trainings) in range(int(nivel.number_initial),int(nivel.number_next_level+1)):
            coach = models_user.User.objects.filter(full_name ="Entrenador Automatico").first()

            models.NivelUser.objects.filter(pk=nivel_user.id).update(nivel=nivel.id,updated_by=coach)
            return f"Congratulations {nivel_user}! You go to {nivel} level"
            


# Multi Query
def multiple_query(list_elem=[]):
   
    list_elements_result=[]
    # Come all subcategory with you id
    for ides in list_elem:
        if type(ides) == list :
            for minilist in ides: 
                
                category_serarch = SubCategory.objects.filter(pk=minilist).only("id","name","code")
                list_elements_result.append(category_serarch)
        else:
            
            category_serarchs = SubCategory.objects.filter(pk=ides).only("id","name","code")
            list_elements_result.append( category_serarchs)

    query  = "select * from (select a.* from catalog_exercise as a"
    # I create the multiquery 
    for index,element in enumerate(list_elements_result):
        if element[0] == list_elements_result[0][0]:
            query += """ INNER JOIN catalog_exercise_sub_category as b
                ON a.id = b.exercise_id 
                Where b.subcategory_id in (%s) ) as primaria """ % (element[0].id)
        else:
            query += """ INNER Join (select a.*, b.subcategory_id as pe from catalog_exercise as a INNER JOIN catalog_exercise_sub_category as b 
        ON a.id = b.exercise_id
        Where b.subcategory_id in (%s) ) as %s
        on primaria.id = %s.id """% (element[0].id,f"a{index}",f"a{index}")
    
    mobility_exer2 = Exercise.objects.raw(query)        
    return mobility_exer2


# Select exercise and filter for equipment
def equip_exer(exercises,exer_for_equip):
    results=[]
    for exercise  in exercises :        
        if exercise in exer_for_equip:
            results.append(exercise)
    return results
            
            
            
#Filter ejer for type , zone
def type_zone(types,zone=[]):
    exercise_type_zone = []
    ids=[]
    if zone ==[]:
        
        exer_type = Exercise.objects.filter(sub_category= types[0].id )
    else:
        # Select id of zone      
        exercicios_zone = Exercise.objects.filter(sub_category__in=zone).filter(sub_category=types[0].id)       
    
    return list(exercicios_zone)

# String to list
def string_list_numeric(string):
    
    if type(string) == int:
        return (int(string))
    
    elif type(string) == str:
        list_string=[]
        
        without_brackets = string.replace("[","").replace("]","")
        for number in without_brackets.split(","):
            list_string.append(int(number))
        return list_string

# Result lack warmup y strenght_secundary
def result( mobility, activation, skills,  strenght_primary, strenght_secundary, esd, stretching, myofascial=[],plyo=[]):
    result= {
        "Myofascial":        [exer for exer in myofascial],
        #"Warmup":            [exer for exer in warmup],
        "Mobility":          [exer for exer in mobility],
        "Activation":        [exer for exer in activation],
        "Skills":            [exer for exer in skills],
        "Plyo":              [exer for exer in plyo],
        "Esd":               [exer for exer in esd],
        "Recovery":          [exer for exer in stretching],
        "Primary Strength":  [exer for exer in strenght_primary],
        "Secondary Strength":[exer for exer in strenght_secundary],

         }
    return result

# Add reps and sets
def reps_sets (values, exercise, user, variation, light_equip, heavy_equip, equip=[],vertical=False,explosive=False):
    # Extract %RM
    per_hundred = models_catalog.BlockExerciseCatalogSubparameter.objects.filter(title="%RM").values("id").first()["id"]  
    result = defaultdict(dict)    
   
    for value in values:
            if (str(value) == "Secondary Strength" or str(value) =="Primary Strength") and len(equip) > 0 :
                for  exer in (exercise[str(value)]):
                    if exer["id"] in light_equip:
                        reps_light = variation_horizontal.sum_variation(string_list_numeric(value.reps_light_equip),variation)

                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],                                   
                                        "sets":value.sets,
                                        "reps":reps_light,
                                        "RIR":value.rir,
                                        "intensity": value.intensity_equipment_RM,
                                        "param_intensity":per_hundred,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                            }
                    elif exer["id"] in heavy_equip:
                        reps_heavy = variation_horizontal.sum_variation(string_list_numeric(value.reps_heavy_equip),variation)

                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],                                    
                                        "sets":value.sets,
                                        "reps":reps_light,
                                        "RIR":value.rir,
                                        "intensity": value.intensity_equipment_RM,
                                        "param_intensity":per_hundred,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                        }
                for  exer in (exercise[str(value)]):
                    if vertical == True and explosive == False :

                        reps_vertical = variation_horizontal.sum_variation(string_list_numeric(value.reps_vertical_jump),variation)                   
                        for index, exer in enumerate(exercise[str(value)]):            
                            result[f"{value.id}"][index]={
                                            "exercise":exer["id"],                                    
                                            "sets":value.sets,
                                            "reps":reps_vertical,
                                            "RIR":value.rir,
                                            "intensity": value.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":value.subparam.id,
                                            "Block type":value.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"], 
                                            }
                    elif  vertical == False and  explosive == True:

                        reps_explosive = variation_horizontal.sum_variation(string_list_numeric(value.reps_explosive),variation)                    
                        for index, exer in enumerate(exercise[str(value)]):            
                            result[f"{value.id}"][index]={
                                            "exercise":exer["id"],                                    
                                            "sets":value.sets,
                                            "reps":reps_explosive,
                                            "RIR":value.rir,
                                            "intensity": value.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":value.subparam.id,
                                            "Block type":value.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                            }
            elif (str(value) == "Secondary Strength" or str(value) =="Primary Strength") and len(equip) == 0 :
                    reps_upper = variation_horizontal.sum_variation(string_list_numeric(value.reps_upper_body_without_equipment),variation)
                    reps_lower = variation_horizontal.sum_variation(string_list_numeric(value.reps_lower_body_without_equipment),variation)

                    for  exer in (exercise[str(value)]):
                        if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:
                            result[f"{value.id}"][index]={
                                                    "exercise":exer["id"],                                    
                                                    "sets":value.sets,
                                                    "reps":reps_lower,
                                                    "RIR":value.rir,
                                                    "intensity": value.intensity_equipment_RM,
                                                    "param_intensity":per_hundred,
                                                    "param":value.subparam.id,
                                                    "Block type":value.block_nivel.block.catalog_block_type.id,
                                                    "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }

                        elif len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Upperr").values("id"))>0:
                            result[f"{value.id}"][index]={
                                                    "exercise":exer["id"],                                               
                                                    "sets":value.sets,
                                                    "reps":reps_upper,
                                                    "RIR":value.rir,
                                                    "intensity": value.intensity_equipment_RM,
                                                    "param_intensity":per_hundred,
                                                    "param":value.subparam.id,
                                                    "Block type":value.block_nivel.block.catalog_block_type.id,
                                                    "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                                    }
            elif   str(value) == "Plyo":
                if len(exercise[str(value)])>0:
                    for index, exer in enumerate(exercise[str(value)]):            
                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],                                       
                                        "sets":value.sets,
                                        "reps":int(value.reps_light_equip)+int(variation)*2,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]                                    
                                        }      
            elif str(value) == "Mobility" or str(value) == "Skills":


                       for index, exer in enumerate(exercise[str(value)]):            
                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],         
                                        "sets":value.sets,
                                        "reps":int(value.reps_light_equip)+int(variation)*2,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name=value).values("id").first()["id"] 
                            }
               

            elif str(value) == "Esd" :
                if  (str(user.nivel) != "Elite" or str(user.nivel) !="Athlete"):


                    for index, exer in enumerate(exercise[str(value)]):            
                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],
                                        "sets":value.sets,
                                        "reps":value.seconds_exercise ,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name="Energy Systems").values("id").first()["id"]                                
                                    }
                else:
                    for index, exer in enumerate(exercise[str(value)]):            
                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],
                                        "sets":value.sets,
                                        "reps":round((value.seconds_exercise)+(0.2*float(variation)),2) ,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name="Energy Systems").values("id").first()["id"]                                
                                    }
            else:
                if  (str(user.nivel) != "Elite" or str(user.nivel) !="Athlete"):
               
                    for index, exer in enumerate(exercise[str(value)]):            
                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],                                  
                                        "sets":value.sets,
                                        "reps":(value.seconds_exercise) ,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name=value).values("id").first()["id"]                                
                                        }
                else:
                     for index, exer in enumerate(exercise[str(value)]):            
                        result[f"{value.id}"][index]={
                                        "exercise":exer["id"],                                            
                                        "sets":value.sets,
                                        "reps":round((value.seconds_exercise)+(0.2*float(variation)),2) ,
                                        "param":value.subparam.id,
                                        "Block type":value.block_nivel.block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name=value).values("id").first()["id"]                                
                                        }

    return dict(result)
# Get the id of the body region of the exercises
def zone_body(exer=[]):    
    body ={}
    ides = []
    if exer != []:
        for e in exer:
            ides.append(e["id"])       
        
        zone = models_catalog.SubCategory.objects.filter(exercise__in=ides,category__category_level_id__name="Region").values("id")
        for bod in  zone:
            if bod["id"] in body:
                body.update({
                        bod["id"]: (int(body[bod["id"]]) +1)
                        })
            else:
                body.update({
                            bod["id"]: 1
                        })           
    return body
  
  
# Take a list of zone id to train Upper  , Lower , etc 
def extract_id_zones(list_zone):
    list_zone_id =[]
    for element  in list_zone:
        list_zone_id.append(element.id)
    return list_zone_id


# Stretching Exercise for zone
def stt_ejercicios(lista):
    stretching = SubCategory.objects.filter(code="STT")

    exercises_stt = []
    for ides in lista:
        exercises_stretching = multiple_query([stretching[0].id,ides])
        for exer in exercises_stretching:
            exercises_stt.append(exer)
    
    return exercises_stt



# String to numerical List

    
def updated_trainings_user(usuario):
    nivel = models.Nivel.objects.get(name ="Elite")

    if usuario.quantity_trainings:
        if int(usuario.quantity_trainings) == int(nivel.number_initial):
            return "You are a Elite Athlete"
       
        else:
            models.NivelUser.objects.filter(pk=usuario.id).update(quantity_trainings=int(usuario.quantity_trainings)+1)
            return "Updated quantity trainings %s" % (int(usuario.quantity_trainings)+1)
   
    else:
        models.NivelUser.objects.filter(pk=usuario.id).update(quantity_trainings=1)
        return "Updated quantity trainings %s" % (1)

# create new item category user

def get_or_create_category_user(level, category):
    #get if exist
    item = models.CategorySelectionNivelUser.objects.filter(
        category_selection=category,
        nivel_user=level
        ).first()

    if item:
        # if exist activate now 
        item.active=True
        item.save()
    else:
        # create new item
        item = models.CategorySelectionNivelUser.objects.create(
            category_selection_id=category,
            nivel_user_id=level,
            active=True
            )
        item.save()
        
def get_or_create_equipment_user(user, equip):
    #get if exist
    item = models.EquipUser.objects.filter(
        equipment = equip,
        user = user).first()
    if  item:
        pass
    else:
        item = models.EquipUser.objects.filter(
        equipment=equip,
        user= user).first()
        item.save()
    
