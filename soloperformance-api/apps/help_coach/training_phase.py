from collections import defaultdict
from apps.catalog import models as models_catalog
from apps.help_coach import models as models_help, utils as utils_help, template_workout, variation_vertical



def training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil):
    total_workouts_week=defaultdict(dict)
    list_exer_realize=[] 
    if week["week_day"]:
        if week["weekvariationhorizontal"] != None:
            if int(week["weekvariationhorizontal"]) == 2 :# =reps = exer
                
                for index,days in enumerate(weeks_days_training[week["id"]]):
                    rise = 0
                    weeks_days,exer_select=utils_help.load_exercise(regiones_id,nivel_user,template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil,list_exer_realize,rise)
                    total_workouts_week[f"{week['id']}"][f"{index}"]={days: weeks_days}

                    list_exer_realize += exer_select

            elif  int(week["weekvariationhorizontal"]) == 3 :# !=reps, = exer 
                count=0
                for index,days in enumerate(weeks_days_training[week["id"]]):
        
                    list_exer_realize = []
                    rise = count
                    count+1
                    weeks_days,exer_select=utils_help.load_exercise(regiones_id,nivel_user,template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil,list_exer_realize,rise)
                    total_workouts_week[f"{week['id']}"][f"{index}"]={days: weeks_days}
                    
            elif  int(week["weekvariationhorizontal"]) == 4 :# !=reps, != exer       
                count=0

                for index,days in enumerate(weeks_days_training[week["id"]]):
        
                    rise = count
                    count+1
                    weeks_days,exer_select=utils_help.load_exercise(regiones_id,nivel_user,template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil,list_exer_realize,rise)
                    total_workouts_week[f"{week['id']}"][f"{index}"]={days: weeks_days}
                    list_exer_realize += exer_select


            elif  int(week["weekvariationhorizontal"]) == 1 :# =reps, = exer                

                for index,days in enumerate(weeks_days_training[week["id"]]):
        
                    list_exer_realize = []
                    rise = 0
                    weeks_days,exer_select=utils_help.load_exercise(regiones_id,nivel_user,template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil,list_exer_realize,rise)
                    total_workouts_week[f"{week['id']}"][f"{index}"]={days: weeks_days}
        else: 
            
         for index,days in enumerate(weeks_days_training[week["id"]]):
            
                    list_exer_realize = []
                    rise = 0
                    weeks_days,exer_select=utils_help.load_exercise(regiones_id,nivel_user,template,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil,list_exer_realize,rise)
                    total_workouts_week[f"{week['id']}"][f"{index}"]={days: weeks_days}
                    
    return total_workouts_week







def variation_vertical_horizontal(program, nivel_user):
    phases = models_catalog.Phase.objects.filter(program =program).filter(active=True).values("id","phase_week","order","variationverticalprogram")
    #weeks = models_catalog.Week.objects.filter(phase=phases[0]["id"]).filter(active=True).values('id',"week_day","weekvariationhorizontal")
    #phases=models_catalog.Phase.objects.filter(program =62).filter(active=True).values("id","phase_week","order","variationverticalprogram")
    weeks_days={}
    workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil = template_workout.template_workout(nivel_user)
    weeks_days_training= defaultdict(list)
    
    for phase in phases:
        weeks = models_catalog.Week.objects.filter(phase=phase["id"]).filter(active=True).values('id',"week_day","weekvariationhorizontal")
        for days in (weeks):
            
            day = []
            day.append((days["week_day"] ))
            weeks_days_training[days['id']] += day
        
        for week,days in weeks_days_training.items():
            
            if  days == [] or days[0] == None:
                weeks_days_training[week]=[]
                
            else:    
                weeks_days_training[week] = list(set(days))
         
    program_workouts= defaultdict(dict)
    week_train = [] 
    for phase in  phases:
        weeks = models_catalog.Week.objects.filter(phase=phase["id"]).filter(active=True).values('id',"week_day","weekvariationhorizontal")     
        regiones_id=[]
        regiones_id = utils_help.extract_regions(phase["id"])
        
            
        variation_phase  = models_help.VariationVertical.objects.filter(pk = phase['variationverticalprogram'] ).values("intensity",'volumen').first()
        for week in weeks:
            count= 0
            if phase["phase_week"] ==  week['id'] and week['id'] not in week_train:

                week_train.append(phase["phase_week"])
                if weeks_days_training[ phase["phase_week"]] :
                    if phase["variationverticalprogram"] == 4:# "Undolating"
                        
                        templates = variation_vertical.change_variation__vertical_intensity_volumen(workout_templates,variation_phase["volumen"],variation_phase['intensity']) 
                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                        count+=1

                    
                    elif  phase["variationverticalprogram"] == 2:# Constant
                        
                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
                    
                    elif phase["variationverticalprogram"] == 5: #Reverse                        

                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
                    elif phase["variationverticalprogram"] == 3: #Linear                        

                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    else:
                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
            
            elif phase["phase_week"] ==  week['id'] and week['id'] in week_train:
                
                if weeks_days_training[ phase["phase_week"]] :

                    if phase["variationverticalprogram"] == 4:# "Undolating"
                        if count%2 == 0:
                            
                            weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                            program_workouts[phase["id"]].update( weeks_days)
                            count += 1
                            
                        elif count%2 != 0:
                            templates = variation_vertical.change_variation__vertical_intensity_volumen(workout_templates,variation_phase["volumen"],variation_phase['intensity'])

                            weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                            program_workouts[phase["id"]].update( weeks_days)
                            count += 1

                    
                    elif  phase["variationverticalprogram"] == 2:# Constant
                        
                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
                    
                    elif  phase["variationverticalprogram"] == 3:#Linear
                        templates = variation_vertical.change_variation__vertical_intensity_volumen(workout_templates,variation_phase["volumen"],variation_phase['intensity'])

                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
                    elif phase["variationverticalprogram"] == 5:# Reverse


                        templates = variation_vertical.change_variation__vertical_intensity_volumen(workout_templates,variation_phase["volumen"],variation_phase['intensity'])

                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
                    else:
                        weeks_days = training_phase_weeks(regiones_id,week,  weeks_days_training,nivel_user,workout_templates,activation,recovery, esd,streng_secundary, streng_primary,plyo,mob,myo,skil)
                        program_workouts[phase["id"]].update( weeks_days)
                    
                   
                      
    return dict(program_workouts)