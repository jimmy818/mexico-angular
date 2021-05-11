import datetime 

# list id exercises by workout
def exericse_id_workout(workout):
    exercises_id =[] 
    for keys, values  in workout.items():
        for val in (values):
            if keys != "Recovery" and val :
                exercises_id.append(values[val]['exercise'])
             
    return exercises_id



# count increment load week 
def increment_load_week_count_id_exercise(workout):
    count= 0
    week = datetime.date.today().strftime("%V")
    exe_id_all_week = []
    try:
        for work in workout:
           
            if work["phase"].strftime("%V") == week and work['accomplished']:

                count+=1
                exe_id_all_week += exericse_id_workout(work["workout"])
         

    except:
        
        if work["phase"].strftime("%V") == week and work["accomplished"]:
                    count+=1
                    exe_id_all_week += exericse_id_workout(work["workout"])
       
    return count , exe_id_all_week

# Increase reps by variation
def sum_variation(list_elem, variation):
    new_list = []
    if type(list_elem ) ==int  :
        return round(list_elem * (variation/100+ 1),0)
    elif type(list_elem) == float:
        return round(list_elem * (variation/100+ 1),2)
    else:
        for number in list_elem:
            new_list.append(round(number * (variation/100+ 1),0))
        return new_list

# Variation decrement in reps  
def decrement_variation(list_elemt ,variation):
    new_list = []
    if type(list_elemt ) ==int:
        return list_elemt - variation*2
    else:
        for number in list_elemt:
            new_list.append(number - variation*2)
        return new_list


# Select exercise are not repeat
def pop_exercise_variation_hotizontal_unequal(exercises_equip, exer_other_trainings):
    new_list=[]
    
    for exer in exercises_equip:
        if exer["id"] not in  set(exer_other_trainings):
            new_list.append(exer)
    return new_list