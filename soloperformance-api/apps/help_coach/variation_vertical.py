





def change_variation__vertical_intensity_volumen(templates,reps,intensity):
    template= templates.copy()
    for types in template:
        template[types]["reps"]= variation_horizontal(template[types]["reps"],reps)
        try:
            template[types]["intensity"] = round(template[types]["intensity"]* ((intensity/100)+1),0)
            
        except: 
            pass
    
    return template



def variation_horizontal(list_elem, variation):
    new_list = []
    if type(list_elem ) == int  :
        return round(int(list_elem * ((int(variation)/100)+1)),0)
    elif type(list_elem) == float:
        return round((list_elem * ((int(variation)/100)+1)),2)
    else:
        for number in list_elem:
            new_list.append(round(number* ((int(variation)/100)+1),0))
        return new_list
    
    
    
def variation_horizontal_undolating(list_elem, variation,number_week):
    new_list = []
    if number_week%2 == 0:
        if type(list_elem ) == int  :
            return list_elem *  variation
        elif type(list_elem) == float:
            return list_elem *  variation
        else:
            for number in list_elem:
                new_list.append(number+variation)
        return new_list

    else:      

        return list_elem
    
    
    
    
def change_variation_vertical_intensity_volumen_reverse(templates,reps,intensity,count):
    template= templates.copy()
    if count == 0:

        for types in template:
            template[types]["reps"] = variation_horizontal_reverse(templates[types]["reps"],reps)

            try:
                template[types]["intensity"] = round(template[types]["intensity"]+(templates[types]["intensity"] * (intensity/100)),0)


            except: 
                pass
        return template
    else :   
        for types in template:
            template[types]["reps"]= variation_horizontal(template[types]["reps"],reps)
            try:
                template[types]["intensity"] = round(template[types]["intensity"]+(template[types]["intensity"] * (intensity/100)),0)
            except: 
                pass
        return template

def variation_horizontal_reverse(list_elem, variation):
    new_list = []
    if type(list_elem ) == int  :
        return int(round((list_elem + list_elem *  variation/100),0))
    elif type(list_elem) == float:

        return  round((list_elem + list_elem  *  variation/100),2)
    else:   
        for number in list_elem:

            new_list.append(int(round(( number + number *   variation/100),0)))
        return new_list