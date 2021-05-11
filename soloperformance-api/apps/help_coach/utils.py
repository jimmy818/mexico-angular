from apps.catalog.models import  Exercise


from operator import itemgetter
from . import models as models_help
from collections import defaultdict
from apps.coach import utils ,models as models_coach, variation_horizontal
from apps.catalog import models as models_catalog
import datetime



def extract_type_quantity_exercise(exdict):
    from collections import defaultdict

    all_types=defaultdict(dict)
    for key, values in exdict.items():
        for key2 , value2 in values.items():
            if str(key) == "Base":
                all_types[str(key)][key2]= values[key2]

            elif  int(values[key2]) >= 0:
                all_types[str(key)][key2]= values[key2]
            else:
                all_types[str(key)][key2]= 0
    return dict(all_types)






def quantity_exer_base(dictionary):
    new_list=defaultdict(dict)
    for key, value in dictionary.items():
        
        for key2, value2 in value.items():                       
            if str(key) != "Base" and int(value2) <= 0:                
                if key not in new_list.keys():  
                    new_list["Base"][key2] = new_list["Base"][key2]+value2       
                         
            elif str(key) == "Base":
                new_list["Base"]=value
                
            elif str(key) != "Base" and int(value2) > 0:                
                  new_list[str(key)][key2]=value2
     
    return dict(new_list)

# sum value dicts
def sum_value_dict( dict_1, dict_2):
    for index,value in zip(list(dict_1.keys()), list(dict_1.values())):
        for index2,value2 in dict_2.items():
            if index == index2:
                dict_1.update({index: value+value2})
            else:
                dict_1[index2] = value2
                
    return dict_1

# Select random exercise by types and options
def exercises_types(exercises_do,region,regions_primary,regions_secundary,heavy_equip,light_equip,user,exer_equip ,equip=[],explosive=False,vertical=False):
    # type exercises
    myo = models_coach.BlockNivel.objects.filter(block__type_exercise="Myofascial").filter(nivel=user.nivel).values("id").first()
    mob = models_coach.BlockNivel.objects.filter(block__type_exercise="Mobility").filter(nivel=user.nivel).values("id").first()
    skil = models_coach.BlockNivel.objects.filter(block__type_exercise="Skills").filter(nivel=user.nivel).values("id").first()
    plyo = models_coach.BlockNivel.objects.filter(block__type_exercise="Plyo").filter(nivel=user.nivel).values("id").first()
    streng_primary = models_coach.BlockNivel.objects.filter(block__type_exercise="Primary Strength").filter(nivel=user.nivel).values("id").first()
    streng_secundary = models_coach.BlockNivel.objects.filter(block__type_exercise="Secondary Strength").filter(nivel=user.nivel).values("id").first()
    esd = models_coach.BlockNivel.objects.filter(block__type_exercise="Esd").filter(nivel=user.nivel).values("id").first()
    recovery = models_coach.BlockNivel.objects.filter(block__type_exercise="Recovery").filter(nivel=user.nivel).values("id").first()
    activation = models_coach.BlockNivel.objects.filter(block__type_exercise="Activation").filter(nivel=user.nivel).values("id").first()
    per_hundred = models_catalog.BlockExerciseCatalogSubparameter.objects.filter(title="%RM").values("id").first()["id"]  


    # Regions primary and secundary
    
    
    upper_pre = models_catalog.SubCategory.objects.filter(category__category_level__name="Region",category__name= ("Upper")).values('id')
    lower_pre = models_catalog.SubCategory.objects.filter(category__category_level__name="Region",category__name= ("Lower")).values('id')
         
    all_zones = [value["id"]for value in  upper_pre]+[value["id"]for value in  lower_pre]

    result = defaultdict(dict)
    war_body ={}
    for values in exercises_do: 
        # Select type for coach
        if values['name'] != 1 :
            if values['block_nivel'] == myo['id']:
                myofascial_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = region).filter(sub_category__code="MYO").values("id"),exer_equip)
                if myofascial_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel= myo['id']).first()

                    myofascial_region_aleatory= utils.random_exercises(myofascial_region, (values['quantity_exercise']))                
                    war_body = sum_value_dict(utils.zone_body(myofascial_region_aleatory),war_body)
                    for index,exer in enumerate(myofascial_region_aleatory):
                        result[f"{myo['id']}"][index]={
                                                "exercise":exer["id"],                                                                                       
                                                "sets":options.sets,
                                                "reps":(options.seconds_exercise) ,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Myofascial').values("id").first()["id"]                                
                                }
            elif values['block_nivel'] == mob["id"] :

                mobility_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = region).filter(sub_category__code="MOB").values("id"),exer_equip)
                if mobility_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel=  mob["id"]).first()
                    mobility_region_aleatory= utils.random_exercises(mobility_region, (values["quantity_exercise"]))  
                    war_body = sum_value_dict(utils.zone_body(mobility_region_aleatory),war_body)
                    for index,exer in enumerate(mobility_region_aleatory):
                        result[f"{mob['id']}"][index]={
                                                "exercise":exer["id"],                                                                                      
                                                "sets":options.sets,
                                                "reps":int(options.reps_light_equip),
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Mobility').values("id").first()["id"] 
                                    }
            elif values['block_nivel'] == skil["id"]  :

                skills_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = region).filter(sub_category__code="SKL").values("id"),exer_equip)

                if skills_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel=  skil["id"]).first()
                    skills_region_aleatory= utils.random_exercises(skills_region, (values["quantity_exercise"]))  
                    war_body = sum_value_dict(utils.zone_body(skills_region_aleatory),war_body)
                    for index,exer in enumerate(mobility_region_aleatory):
                        result[f"{ skil['id']}"][index]={
                                                "exercise":exer["id"],                                                                                      
                                                "sets":options.sets,
                                                "reps":int(options.reps_light_equip),
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Skills').values("id").first()["id"] 
                                    }

            elif values['block_nivel'] == streng_primary["id"]  :

                primary_strength_region= utils.equip_exer(Exercise.objects.filter(sub_category__in=regions_primary).filter(sub_category__code="STR").values("id"),exer_equip)
                if primary_strength_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel=  streng_primary["id"]).first()
                    primary_strength_region_aleatory= utils.random_exercises(primary_strength_region, (values["quantity_exercise"])) 
                    war_body = sum_value_dict(utils.zone_body(primary_strength_region_aleatory),war_body)
                    if len(equip) > 0 and (vertical == False and explosive == False ):
                        for index,exer in enumerate(primary_strength_region_aleatory):
                            if exer["id"] in light_equip:
                                 result[f"{streng_primary['id']}"][index]={
                                            "exercise":exer["id"],                                   
                                            "sets":options.sets,
                                            "reps":options.reps_light_equip,
                                            "RIR":options.rir,
                                            "intensity": options.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                }
                            if exer["id"] in heavy_equip: 
                                result[f"{streng_primary['id']}"][index]={
                                            "exercise":exer["id"],                                   
                                            "sets":options.sets,
                                            "reps":options.reps_heavy_equip,
                                            "RIR":options.rir,
                                            "intensity": options.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                }
                    elif len(equip) > 0 and (vertical == True and explosive == False) :
                            for index,exer in enumerate(primary_strength_region_aleatory):
                                     result[f"{streng_primary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_vertical_jump,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip) > 0 and (vertical == False and explosive == True) :
                            for index,exer in enumerate(primary_strength_region_aleatory):
                                    result[f"{streng_primary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_explosive,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip)  == 0:# Without Equip
                            for index,exer in enumerate(primary_strength_region_aleatory):
                                if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:

                                    result[f"{streng_primary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_lower_body_without_equipment,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                                elif len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Upper").values("id"))>0:

                                    result[f"{streng_primary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_upper_body_without_equipment,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }


            elif values['block_nivel'] == streng_secundary["id"] :
                options = models_coach.SetsReps.objects.filter(block_nivel=  streng_secundary["id"]).first()

                secondary_strength_region= utils.equip_exer(Exercise.objects.filter(sub_category__in=regions_secundary).filter(sub_category__code="STR").values("id"),exer_equip)
                if secondary_strength_region:


                    secondary_strength_region_aleatory= utils.random_exercises(secondary_strength_region, (values["quantity_exercise"])) 

                    war_body = sum_value_dict(utils.zone_body(secondary_strength_region_aleatory),war_body)

                    if len(equip) > 0 and (vertical == False and explosive == False) :#with Equipment
                        for index,exer in enumerate(secondary_strength_region_aleatory):
                            if exer["id"] in light_equip:#Equipment light
                                 result[f"{streng_secundary['id']}"][index]={
                                            "exercise":exer["id"],                                   
                                            "sets":options.sets,
                                            "reps":options.reps_light_equip,
                                            "RIR":options.rir,
                                            "intensity": options.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                }
                            if exer["id"] in heavy_equip: #Equipment heavy
                                result[f"{streng_secundary['id']}"][index]={
                                            "exercise":exer["id"],                                   
                                            "sets":options.sets,
                                            "reps":options.reps_heavy_equip,
                                            "RIR":options.rir,
                                            "intensity": options.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                }
                    elif len(equip) > 0 and (vertical == True and explosive == False) :
                            for index,exer in enumerate(secondary_strength_region_aleatory):
                                     result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_vertical_jump,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip) > 0 and (vertical == False and explosive == True) :
                            for index,exer in enumerate(secondary_strength_region_aleatory):
                                    result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_explosive,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip)  == 0:# Without Equip
                            for index,exer in enumerate(secondary_strength_region_aleatory):
                                if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:

                                    result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_lower_body_without_equipment,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                                elif len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Upper").values("id"))>0:

                                    result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_upper_body_without_equipment,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }

            elif values['block_nivel'] == plyo["id"]  :

                plyo_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = all_zones).filter(sub_category__code="PLY").values("id"),exer_equip)

                if plyo_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel=  plyo["id"]).first()
                    plyo_region_region_aleatory= utils.random_exercises(plyo_region, (values["quantity_exercise"]))
                    war_body = sum_value_dict(utils.zone_body(plyo_region_region_aleatory),war_body)
                    for index,exer in enumerate(plyo_region_region_aleatory):
                            result[f"{plyo['id']}"][index]={
                                            "exercise":exer["id"],                                       
                                            "sets":options.sets,
                                            "reps":int(options.reps_light_equip),
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]                                    
                                            }  

        # Basic exercises
        else:
            if values['block_nivel'] == myo["id"]:
                myofascial_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = all_zones).filter(sub_category__code="MYO").values("id"),exer_equip)

                if myofascial_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel= myo['id']).first()
                    myofascial_region_aleatory= utils.random_exercises(myofascial_region, (values["quantity_exercise"]))                
                    war_body = sum_value_dict(utils.zone_body(myofascial_region_aleatory),war_body)
                    for index,exer in enumerate(myofascial_region_aleatory):
                        result[f"{myo['id']}"][index]={
                                                "exercise":exer["id"],                                                                                       
                                                "sets":options.sets,
                                                "reps":(options.seconds_exercise) ,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Myofascial').values("id").first()["id"]                                
                                    }


            elif values['block_nivel'] == mob["id"]:
                mobility_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = all_zones).filter(sub_category__code="MOB").values("id"),exer_equip)
                options = models_coach.SetsReps.objects.filter(block_nivel= mob["id"]).first()

                if mobility_region:
                    mobility_region_aleatory= utils.random_exercises(mobility_region, (values["quantity_exercise"])) 
                    war_body = sum_value_dict(utils.zone_body(mobility_region_aleatory),war_body)
                    for index, exer in enumerate(mobility_region_aleatory):
                        result[f"{mob['id']}"][index]={
                                            "exercise":exer["id"],         
                                            "sets":options.sets,
                                            "reps":int(options.reps_light_equip),
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Mobility').values("id").first()["id"] 
                                }


            elif values['block_nivel'] == activation["id"]:
                activation_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = all_zones).filter(sub_category__code="CORE").values("id"),exer_equip)
                options = models_coach.SetsReps.objects.filter(block_nivel=  activation["id"]).first()

                if activation_region:

                    activation_region_aleatory= utils.random_exercises(activation_region, (values["quantity_exercise"]))  
                    war_body = sum_value_dict(utils.zone_body(activation_region_aleatory),war_body)
                    for index, exer in enumerate(activation_region_aleatory):
                         result[f"{activation['id']}"][index]={
                                            "exercise":exer["id"],                                            
                                            "sets":options.sets,
                                            "reps":(options.seconds_exercise),
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Activation').values("id").first()["id"]                                
                                            }

            elif values['block_nivel'] == skil["id"]:
                skills_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = all_zones).filter(sub_category__code="SKL").values("id"),exer_equip)

                if skills_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel=  skil["id"]).first()
                    skills_region_aleatory= utils.random_exercises(skills_region, (values["quantity_exercise"]))  
                    war_body = sum_value_dict(utils.zone_body(skills_region_aleatory),war_body)
                    for index , exer in enumerate(skills_region_aleatory):
                        result[f"{skil['id']}"][index]={
                                            "exercise":exer["id"],         
                                            "sets":options.sets,
                                            "reps":int(options.reps_light_equip),
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Skills').values("id").first()["id"] 
                                }


            elif values['block_nivel'] == streng_primary["id"]:
                options = models_coach.SetsReps.objects.filter(block_nivel=  streng_primary["id"]).first()
                primary_strength_region= utils.equip_exer(Exercise.objects.filter(sub_category__in=regions_primary).filter(sub_category__code="STR").values("id"),exer_equip)
                if primary_strength_region:
                    primary_strength_region_aleatory= utils.random_exercises(primary_strength_region, (values["quantity_exercise"]))  
                    war_body = sum_value_dict(utils.zone_body(primary_strength_region_aleatory),war_body)
                    if len(equip) > 0 and (vertical == False and explosive == False) :
                            for index,exer in enumerate(primary_strength_region_aleatory):
                                if exer["id"] in light_equip:
                                     result[f"{streng_primary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_light_equip,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                                if exer["id"] in heavy_equip: 
                                    result[f"{streng_primary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_heavy_equip,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip) > 0 and (vertical == True and explosive == False) :
                                for index,exer in enumerate(primary_strength_region_aleatory):
                                         result[f"{streng_primary['id']}"][index]={
                                                    "exercise":exer["id"],                                   
                                                    "sets":options.sets,
                                                    "reps":options.reps_vertical_jump,
                                                    "RIR":options.rir,
                                                    "intensity": options.intensity_equipment_RM,
                                                    "param_intensity":per_hundred,
                                                    "param":options.subparam.id,
                                                    "Block type":options.block_nivel.block.catalog_block_type.id,
                                                    "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                        }
                    elif len(equip) > 0 and (vertical == False and explosive == True) :
                                for index,exer in enumerate(primary_strength_region_aleatory):
                                        result[f"{streng_primary['id']}"][index]={
                                                    "exercise":exer["id"],                                   
                                                    "sets":options.sets,
                                                    "reps":options.reps_explosive,
                                                    "RIR":options.rir,
                                                    "intensity": options.intensity_equipment_RM,
                                                    "param_intensity":per_hundred,
                                                    "param":options.subparam.id,
                                                    "Block type":options.block_nivel.block.catalog_block_type.id,
                                                    "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                        }
                    elif len(equip)  == 0:# Without Equip
                                for index,exer in enumerate(primary_strength_region_aleatory):
                                    
                                    if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:

                                        result[f"{streng_primary['id']}"][index]={
                                                    "exercise":exer["id"],                                   
                                                    "sets":options.sets,
                                                    "reps":options.reps_lower_body_without_equipment,
                                                    "RIR":options.rir,
                                                    "intensity": options.intensity_equipment_RM,
                                                    "param_intensity":per_hundred,
                                                    "param":options.subparam.id,
                                                    "Block type":options.block_nivel.block.catalog_block_type.id,
                                                    "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                        }
                                    elif len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Upper").values("id"))>0:

                                        result[f"{streng_primary['id']}"][index]={
                                                    "exercise":exer["id"],                                   
                                                    "sets":options.sets,
                                                    "reps":options.reps_upper_body_without_equipment,
                                                    "RIR":options.rir,
                                                    "intensity": options.intensity_equipment_RM,
                                                    "param_intensity":per_hundred,
                                                    "param":options.subparam.id,
                                                    "Block type":options.block_nivel.block.catalog_block_type.id,
                                                    "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                        }


            elif values['block_nivel'] == streng_secundary["id"]:
                secondary_strength_region= utils.equip_exer(Exercise.objects.filter(sub_category__in=regions_secundary).filter(sub_category__code="STR").values("id"),exer_equip)
                options = models_coach.SetsReps.objects.filter(block_nivel=  streng_secundary["id"]).first()

                if secondary_strength_region:
                    secondary_strength_region_aleatory= utils.random_exercises(secondary_strength_region, (values["quantity_exercise"]))   
                    war_body = sum_value_dict(utils.zone_body(secondary_strength_region_aleatory),war_body)

                    if len(equip) > 0 and(vertical == False and explosive == False ):#with Equipment
                        for index,exer in enumerate(secondary_strength_region_aleatory):
                            if exer["id"] in light_equip:#Equipment light
                                 result[f"{streng_secundary['id']}"][index]={
                                            "exercise":exer["id"],                                   
                                            "sets":options.sets,
                                            "reps":options.reps_light_equip,
                                            "RIR":options.rir,
                                            "intensity": options.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                }
                            if exer["id"] in heavy_equip: #Equipment heavy
                                result[f"{streng_secundary['id']}"][index]={
                                            "exercise":exer["id"],                                   
                                            "sets":options.sets,
                                            "reps":options.reps_heavy_equip,
                                            "RIR":options.rir,
                                            "intensity": options.intensity_equipment_RM,
                                            "param_intensity":per_hundred,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                }
                    elif len(equip) > 0 and (vertical == True and explosive == False) :
                            for index,exer in enumerate(secondary_strength_region_aleatory):
                                     result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_vertical_jump,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip) > 0 and (vertical == False and explosive == True ):
                            for index,exer in enumerate(secondary_strength_region_aleatory):
                                    result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_explosive,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                    elif len(equip) == 0:# Without Equip
                            for index,exer in enumerate(secondary_strength_region_aleatory):
                                if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:

                                    result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_lower_body_without_equipment,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
                                elif len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Upper").values("id"))>0:

                                    result[f"{streng_secundary['id']}"][index]={
                                                "exercise":exer["id"],                                   
                                                "sets":options.sets,
                                                "reps":options.reps_upper_body_without_equipment,
                                                "RIR":options.rir,
                                                "intensity": options.intensity_equipment_RM,
                                                "param_intensity":per_hundred,
                                                "param":options.subparam.id,
                                                "Block type":options.block_nivel.block.catalog_block_type.id,
                                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                                    }
            elif values['block_nivel'] == plyo["id"]:
                plyo_region= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__category__name = all_zones).filter(sub_category__code="PLY").values("id"),exer_equip)
                if plyo_region:
                    options = models_coach.SetsReps.objects.filter(block_nivel=  plyo["id"]).first()

                    plyo_region_region_aleatory= utils.random_exercises(plyo_region, (values["quantity_exercise"]))  
                    war_body = sum_value_dict(utils.zone_body(plyo_region_region_aleatory),war_body)
                    for index, exer in enumerate(plyo_region_region_aleatory):
                        result[f"{plyo['id']}"][index]={
                                            "exercise":exer["id"],                                       
                                            "sets":options.sets,
                                            "reps":int(options.reps_light_equip),
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]                                    
                                            }      

            elif values['block_nivel'] == esd["id"]:
                options = models_coach.SetsReps.objects.filter(block_nivel=  esd["id"]).first()

                exercises_esd = Exercise.objects.filter (sub_category__code = "ESD").values("id")

                esd_region_aleatory= utils.random_exercises(exercises_esd, (values["quantity_exercise"]))  
                war_body = sum_value_dict(utils.zone_body(esd_region_aleatory),war_body)
                for index, exer in enumerate(esd_region_aleatory):
                     result[f"{esd['id']}"][index]={
                                            "exercise":exer["id"],
                                            "sets":options.sets,
                                            "reps":options.seconds_exercise ,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name="Energy Systems").values("id").first()["id"]                 
                                        }

    war_body_sorted = dict(sorted(war_body.items(), key=itemgetter(1),reverse=True))     
        # Exer stretching -- RECOVERY --
    
    for value in exercises_do:
        if recovery['id'] == value['block_nivel']:
            exercises_stretching= Exercise.objects.filter(sub_category__in=list(war_body_sorted)[:(values["quantity_exercise"])]).filter(sub_category__code="STT").values("id") 
            if len(exercises_stretching)>0:
                exercises_stretching_aleatory = utils.random_exercises(exercises_stretching , (values["quantity_exercise"]))
                options = models_coach.SetsReps.objects.filter(block_nivel=  recovery['id']).first()
                for index, exer in enumerate(exercises_stretching_aleatory):
                    result[f"{recovery['id']}"][index]={
                                            "exercise":exer["id"],                                            
                                            "sets":options.sets,
                                            "reps":(options.seconds_exercise) ,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Recovery').values("id").first()["id"]                                
                                            }
        else:
            exercises_stretching= Exercise.objects.filter(sub_category__in=list(war_body_sorted)).filter(sub_category__code="STT").values("id") 
            exercises_stretching_aleatory = utils.random_exercises(exercises_stretching , (values["quantity_exercise"]))
            options = models_coach.SetsReps.objects.filter(block_nivel=  recovery['id']).first()
            for index, exer in enumerate(exercises_stretching_aleatory):
                result[f"{recovery['id']}"][index]={
                                            "exercise":exer["id"],                                            
                                            "sets":options.sets,
                                            "reps":(options.seconds_exercise) ,
                                            "param":options.subparam.id,
                                            "Block type":options.block_nivel.block.catalog_block_type.id,
                                            "icon": models_catalog.Coding.objects.filter(name='Recovery').values("id").first()["id"]                                
                                            }
    return dict(result)



# Place exercises
def place_exercises(type_exer):
    dict_new = defaultdict(dict)
    for index,exers in type_exer.items():
        if str(index) != "Recovery":

            for exer in exers:
                if len(dict_new[exer]) > 0:
                    dict_new[exer]+= exers[exer]
                else:
                    dict_new[exer]= exers[exer]
        else:
            dict_new[index] = exers
    return dict(dict_new)





# variation Vertical
def change_variations_vertical(training,varition,program):
    weeks = models_catalog.Week.objects.filter(phase__program =program)
    week_training = datetime.datetime.now().strftime("%V")
    #week_training = 13
    variation_vert = 0
    if str(varition.name) == "Undolating":
        for index,week in enumerate(weeks)  :
            if int(week.number_week) == int(week_training) and index%2 == 0: 
                variation_vert_intensity = ((index) * int(varition.intensity))
                variation_vert_volumen = ((index) * int(varition.volumen))
                
            elif int(week.number_week) == int(week_training) and index%2 != 0:
                variation_vert_volumen = 0
                variation_vert_intensity = 0
                
                
        for index,train in (training.items()):
            for exer in range(0,len(train)):                
                try:
                    if train[exer]["intensity"] :
                        train[exer]["intensity"] +=  variation_vert_intensity
                    
                except:
                    pass
                if train[exer]["reps"]:
                        train[exer]["reps"] += variation_vert_volumen
                    
    else:  
        for index,week in enumerate(weeks):
            
            if int(week.number_week) == int(week_training):
                variation_vert_intensity = ((index) * int(varition.intensity))
                variation_vert_volumen = ((index) * int(varition.volumen))
                
        for index,train in training.items():
            for exer in range(0,len(train)):
                try:
                    if train[exer]["intensity"] :
                        train[exer]["intensity"] +=  variation_vert_intensity
                    
                except:
                    pass
                if train[exer]["reps"]:
                        train[exer]["reps"] += variation_vert_volumen
                
    return training


def template_workout(user):       
            
    myo = models_coach.BlockNivel.objects.filter(block__type_exercise="Myofascial").filter(nivel=user.nivel).values("id").first()
    mob = models_coach.BlockNivel.objects.filter(block__type_exercise="Mobility").filter(nivel=user.nivel).values("id").first()
    skil = models_coach.BlockNivel.objects.filter(block__type_exercise="Skills").filter(nivel=user.nivel).values("id").first()
    plyo = models_coach.BlockNivel.objects.filter(block__type_exercise="Plyo").filter(nivel=user.nivel).values("id").first()
    streng_primary = models_coach.BlockNivel.objects.filter(block__type_exercise="Primary Strength").filter(nivel=user.nivel).values("id").first()
    streng_secundary = models_coach.BlockNivel.objects.filter(block__type_exercise="Secondary Strength").filter(nivel=user.nivel).values("id").first()
    esd = models_coach.BlockNivel.objects.filter(block__type_exercise="Esd").filter(nivel=user.nivel).values("id").first()
    recovery = models_coach.BlockNivel.objects.filter(block__type_exercise="Recovery").filter(nivel=user.nivel).values("id").first()
    activation = models_coach.BlockNivel.objects.filter(block__type_exercise="Activation").filter(nivel=user.nivel).values("id").first()
    per_hundred = models_catalog.BlockExerciseCatalogSubparameter.objects.filter(title="%RM").values("id").first()["id"]  
    
    result = defaultdict(dict)
   
        
    options = models_coach.SetsReps.objects.filter(block_nivel= myo["id"]).values("sets","seconds_exercise","subparam","block_nivel").first()                       

    result[f"{myo['id']}"]={        "exercise":[],                                                                                       
                                    "sets":options['sets'],
                                    "reps":(options['seconds_exercise']) ,
                                    "param":options['subparam'],
                                    "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                                    "icon": models_catalog.Coding.objects.filter(name='Myofascial').values("id").first()["id"]                                
                        }


    options = models_coach.SetsReps.objects.filter(block_nivel= mob["id"]).values("sets","reps_light_equip","subparam","block_nivel").first()                       

    result[f"{mob['id']}"]={
                                "exercise":[],         
                                "sets":options['sets'],
                                "reps":int(options['reps_light_equip']),
                                "param":options['subparam'],
                                "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                                "icon": models_catalog.Coding.objects.filter(name='Mobility').values("id").first()["id"] 
                    }


    options = models_coach.SetsReps.objects.filter(block_nivel= activation["id"]).values("sets","seconds_exercise","subparam","block_nivel").first()                       


    result[f"{activation['id']}"]={
                                "exercise":[],                                            
                                "sets":options['sets'],
                                "reps":options['seconds_exercise'],
                                "param":options['subparam'],
                                "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                                "icon": models_catalog.Coding.objects.filter(name='Activation').values("id").first()["id"]                                
                                }

    options = models_coach.SetsReps.objects.filter(block_nivel=skil["id"]).values("sets","reps_light_equip","subparam","block_nivel").first()                       

    result[f"{skil['id']}"]={
                                "exercise":[],         
                                "sets":options['sets'],
                                "reps":int(options['reps_light_equip']),
                                "param":options['subparam'],
                                "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                                "icon": models_catalog.Coding.objects.filter(name='Skills').values("id").first()["id"] 
                    }


    options = models_coach.SetsReps.objects.filter(block_nivel=  streng_primary["id"]).values("sets","intensity_equipment_RM","rir","reps_light_equip","subparam","block_nivel").first()                       

    result[f"{streng_primary['id']}"]={
                                        "exercise":[],                                   
                                        "sets":options['sets'],
                                        "reps": utils.string_list_numeric(options['reps_light_equip']),
                                        "RIR":options['rir'],
                                        "intensity": options['intensity_equipment_RM'],
                                        "param_intensity":per_hundred,
                                        "param":options['subparam'],
                                        "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                                        "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]                                  
                    }



    options = models_coach.SetsReps.objects.filter(block_nivel=  streng_secundary["id"]).values("sets","intensity_equipment_RM","rir","reps_light_equip","subparam","block_nivel").first()                       
    result[f"{streng_secundary['id']}"]={
                "exercise":[],                                   
                "sets":options['sets'],
                "reps": utils.string_list_numeric(options["reps_light_equip"]),
                "RIR":options["rir"],
                "intensity": options['intensity_equipment_RM'],
                "param_intensity":per_hundred,
                "param":options['subparam'],
                "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]
                 }

    options = models_coach.SetsReps.objects.filter(block_nivel=  plyo["id"]).values("sets","reps_light_equip","subparam","block_nivel").first()


    result[f"{plyo['id']}"]={
                                "exercise":[],                                       
                                "sets":options['sets'],
                                "reps":int(options['reps_light_equip']),
                                "param":options['subparam'],
                                "Block type":models_coach.BlockNivel.objects.get(pk=options["block_nivel"]).block.catalog_block_type.id,
                                "icon": models_catalog.Coding.objects.filter(name='Strength').values("id").first()["id"]                                    
                                }      

    options_esd = models_coach.SetsReps.objects.filter(block_nivel=  esd["id"]).values("sets","rest_exercise","seconds_exercise","subparam","block_nivel").first()


    result[f"{esd['id']}"]={
                                "exercise":[],
                                "sets":options_esd['sets'],
                                "reps":options_esd['seconds_exercise']  ,
                                "param":options_esd['subparam'],
                                "Block type":models_coach.BlockNivel.objects.get(pk=options_esd["block_nivel"]).block.catalog_block_type.id,
                                "icon": models_catalog.Coding.objects.filter(name="Energy Systems").values("id").first()["id"],                 
                                "rest exercise":options_esd["rest_exercise"],
                                }

        # Exer stretching -- RECOVERY --

    options_recovery = models_coach.SetsReps.objects.filter(block_nivel=  recovery["id"]).values("sets","seconds_exercise","subparam","block_nivel").first()



    result[f"{recovery['id']}"]={
                            "exercise":[],                                            
                            "sets":options_recovery['sets'],
                            "reps":options_recovery['seconds_exercise'] ,
                            "param":options_recovery['subparam'],
                            "Block type":models_coach.BlockNivel.objects.get(pk=options_recovery["block_nivel"]).block.catalog_block_type.id,
                            "icon": models_catalog.Coding.objects.filter(name='Recovery').values("id").first()["id"]                                
                            }

    return result,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo, skil 
    
    
    
# list equip for user 
def list_equip(user):
    equips = models_coach.EquipUser.objects.filter(user=user.user ).values("equipment")
    list_equip=[]
    for equip in equips:
        if equip["equipment"]:
            list_equip.append(equip["equipment"])
    return list_equip


# put_exericse 
def load_exercise(regions_user,user_nivel,workout_template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil,old_workout,increment):
    equip =list_equip(user_nivel)
    equip_exercises  = utils.filter_equipment(equip)
    exercises_equip = variation_horizontal.pop_exercise_variation_hotizontal_unequal(equip_exercises, old_workout)   
        
        
    category_nivel_user_block = models_coach.CategorySelectionNivelUser.objects.filter(nivel_user= user_nivel).values("category_selection")
    category_selections=[]
    vertical = False
    explosive = False
    # Select id of Category
    base = models_coach.Category.objects.filter(name= "Base").values("id").first()

    category_selections.append(base["id"])
    # See types categories 
    for options in category_nivel_user_block:
        category_selections.append(options["category_selection"])
        if int(options['category_selection'])== 7:
            vertical = True
        elif int(options['category_selection'])== 8:
            explosive = True
            
    # # Regions primary and secundary and equip heavy or light       
    regions = models_coach.HierarchyRegions.objects.all().values("name","region")
    regions_primary, regions_secundary , heavy_equip, light_equip= utils.hierarchy_regions_id(regions)
            
    # Quantity of exercises and type
    exercise_type_quantity = models_coach.CategorySelection.objects.filter(name_id__in=category_selections,block_nivel__nivel= user_nivel.nivel).values("block_nivel",'quantity_exercise',"name")
    list_exercises=[]
    for value in exercise_type_quantity:
        if int(value['quantity_exercise']) >0 :
            list_exercises.append(value)
    
    result = defaultdict(dict)
    war_body={}
    options_streng_primary = models_coach.SetsReps.objects.filter(block_nivel=  streng_primary["id"]).values("reps_heavy_equip","reps_lower_body_without_equipment","reps_upper_body_without_equipment","reps_vertical_jump","reps_explosive").first()
    options_streng_secundary = models_coach.SetsReps.objects.filter(block_nivel=  streng_primary["id"]).values("reps_heavy_equip","reps_lower_body_without_equipment","reps_upper_body_without_equipment","reps_vertical_jump","reps_explosive").first()
    exer_select=[]
    traninig_done = []
    for list_exercise in list_exercises:

        if   int(streng_primary["id"]) == int(list_exercise["block_nivel"])  and int(streng_primary["id"]) not in  traninig_done:
            traninig_done.append(int(streng_primary["id"]))
            exercises = utils.equip_exer(Exercise.objects.filter(sub_category__in=regions_primary).filter(sub_category__code="STR").values("id"),exercises_equip)
            exercise_aleatory = utils.random_exercises(exercises,list_exercise['quantity_exercise'])
            exer_select += [exercise["id"] for exercise in exercise_aleatory]
            war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
            molde = workout_template[str(list_exercise["block_nivel"])].copy()
            result[str(list_exercise["block_nivel"])][index] = molde.copy()

            if len(equip)== 0:
                for index,exer in enumerate(exercise_aleatory):
                    
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:
                        
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_primary["reps_lower_body_without_equipment"]),increment)
                    else:
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_primary["reps_upper_body_without_equipment"]),increment)

                        
            elif len(equip) >0 and (vertical == False and explosive == False):
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    if exer["id"] in heavy_equip:                        
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_primary["reps_heavy_equip"]),increment)
                    else:                       
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)

            elif len(equip) >0 and (vertical == True and explosive == False):
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_primary["reps_vertical_jump"]),increment)
            
            elif len(equip) >0 and (vertical == False and explosive == True):
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_primary["reps_explosive"]),increment)



        elif   int(streng_secundary["id"]) == int(list_exercise["block_nivel"]) and int(streng_secundary["id"]) not in  traninig_done:
            traninig_done.append(int(streng_secundary["id"]))

            exercises = utils.equip_exer(Exercise.objects.filter(sub_category__in=regions_secundary).filter(sub_category__code="STR").values("id"),exercises_equip)
            exercise_aleatory = utils.random_exercises(exercises,list_exercise['quantity_exercise'])
            exer_select += [exercise["id"] for exercise in exercise_aleatory]

            war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
            molde = workout_template[str(list_exercise["block_nivel"])].copy()

            if len(equip)== 0:
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    if len(models_catalog.SubCategory.objects.filter(exercise=exer["id"],category__category_level__name="Region",category__name="Lower").values("id"))>0:
                        
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_secundary["reps_lower_body_without_equipment"]),increment)
                    else:
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_secundary["reps_upper_body_without_equipment"]) ,increment)

                        
            elif len(equip) >0 and (vertical == False and explosive == False):
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    if exer["id"] in heavy_equip:                        
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_secundary["reps_heavy_equip"]),increment)
                    else:                       
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)

            elif len(equip) >0 and (vertical == True and explosive == False):
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_secundary["reps_vertical_jump"]),increment)
            
            elif len(equip) >0 and (vertical == False and explosive == True):
                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(utils.string_list_numeric(options_streng_secundary["reps_explosive"]),increment)


        elif int(mob["id"])  == int(list_exercise["block_nivel"]) and int(mob["id"])  not in  traninig_done:
            traninig_done.append(int(mob["id"]) )
            exercises= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" , sub_category__in = regions_user).filter(sub_category__code="MOB").values("id"), exercises_equip)

            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercise_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                exer_select += [exercise["id"] for exercise in exercise_aleatory]
                
                war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()
                

                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)
            else:
                exercises= utils.equip_exer(Exercise.objects.filter(sub_category__category__category_level__name="Region" ).filter(sub_category__code="MOB").values("id"), exercises_equip)
                if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                    exercise_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                    exer_select += [exercise["id"] for exercise in exercise_aleatory]
                    
                    war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                    molde = workout_template[str(list_exercise["block_nivel"])].copy()
                    

                    for index,exer in enumerate(exercise_aleatory):
                        result[str(list_exercise["block_nivel"])][index] = molde.copy()
                        result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)
           

        elif   int(activation["id"]) == int(list_exercise["block_nivel"]) and int(activation["id"]) not in traninig_done:
            traninig_done.append(int(activation["id"]))
            exercises= utils.equip_exer(Exercise.objects.filter(sub_category__code="CORE").values("id"),exercises_equip)
            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercise_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                exer_select += [exercise["id"] for exercise in exercise_aleatory]

                war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()

                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)

        elif  int(myo["id"]) == int(list_exercise["block_nivel"]) and  int(myo["id"]) not in  traninig_done:
            traninig_done.append(int(myo["id"]))
            exercises= utils.equip_exer(Exercise.objects.filter(sub_category__code="MYO").values("id"),exercises_equip)
            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercise_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                exer_select += [exercise["id"] for exercise in exercise_aleatory]

                war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()


                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)


        elif int(skil["id"]) == int(list_exercise["block_nivel"]) and int(skil["id"]) not in  traninig_done:
            traninig_done.append(int(skil["id"]))
            exercises= utils.equip_exer(Exercise.objects.filter(sub_category__code="SKL", sub_category__in = regions_user).values("id"),exercises_equip)
            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercises_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                exer_select += [exercise["id"] for exercise in exercise_aleatory]

                war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()


                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)
            else:
                exercises= utils.equip_exer(Exercise.objects.filter(sub_category__code="SKL").values("id"),exercises_equip)
                if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                    exercises_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                    exer_select += [exercise["id"] for exercise in exercise_aleatory]

                    war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                    molde = workout_template[str(list_exercise["block_nivel"])].copy()


                    for index,exer in enumerate(exercise_aleatory):
                        result[str(list_exercise["block_nivel"])][index] = molde.copy()
                        result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]
                        result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)

                

        elif int(plyo["id"]) == int(list_exercise["block_nivel"]) and int(plyo["id"]) not in  traninig_done:
            traninig_done.append(int(plyo["id"]))
            exercises= utils.equip_exer(Exercise.objects.filter(sub_category__code="PLY").values("id"),exercises_equip)
            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercises_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                exer_select += [exercise["id"] for exercise in exercise_aleatory]

                war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()


                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]         
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)

        elif int(esd["id"]) == int(list_exercise["block_nivel"]) and int(esd["id"]) not in  traninig_done:
            traninig_done.append(int(esd["id"]))
            exercises= Exercise.objects.filter(sub_category__code="PLY").values("id")
            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercises_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                exer_select += [exercise["id"] for exercise in exercise_aleatory]

                war_body = sum_value_dict(utils.zone_body(exercise_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()


                for index,exer in enumerate(exercise_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"]         
                    result[str(list_exercise["block_nivel"])][index]["reps"] = variation_horizontal.sum_variation(result[str(list_exercise["block_nivel"])][index]["reps"],increment)

                    
                    
                    
    war_body_sorted = dict(sorted(war_body.items(), key=itemgetter(1),reverse=True))     
    for list_exercise in list_exercises:
        if   int(recovery["id"]) == int(list_exercise["block_nivel"]):

            exercises= Exercise.objects.filter(sub_category__in=(list(war_body_sorted))).filter(sub_category__code="STT").values("id")
            if exercises and len(exercises) >= list_exercise['quantity_exercise']:
                exercises_aleatory= utils.random_exercises(exercises,list_exercise['quantity_exercise'])
                war_body = sum_value_dict(utils.zone_body(exercises_aleatory),war_body)
                molde = workout_template[str(list_exercise["block_nivel"])].copy()


                for index,exer in enumerate(exercises_aleatory):
                    result[str(list_exercise["block_nivel"])][index] = molde.copy()
                    result[str(list_exercise["block_nivel"])][index]["exercise"] = exer["id"] 
                    
    return dict(result),exer_select



# Extract Regions
def extract_regions(phase):
    regions_id =[]

    if models_help.RegionsCategoryCoach.objects.filter(phase=phase ).exists():
        regions = models_help.RegionsCategoryCoach.objects.filter(phase=phase ).values("regions")
        for reg in regions:
            if reg["regions"] != None:
                regions_id.append(reg["regions"])
        return regions_id
    else:
        regions = models_catalog.SubCategory.objects.filter(category__category_level__name="Region").values("id")
        for reg in regions:
            if reg["id"] != None:
                regions_id.append(reg["id"])
        return regions_id
    