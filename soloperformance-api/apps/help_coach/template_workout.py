from apps.coach import utils ,models as models_coach, variation_horizontal
from apps.catalog import models as models_catalog
from collections import defaultdict
from operator import itemgetter




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