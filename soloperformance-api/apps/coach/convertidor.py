# convertidor de métricas.
class Convertidor:
    
    def __init__(self):
        dato = self.dato
        tipo = self.tipo 
        original = self.original

    
    def weight(dato , tipo):
        
        if str(tipo).lower() == "absolute (lbs)":
            result = dato / 0.45359265
            return round(result ,2)
        
        elif str(tipo).lower() == "absolute (kg)":
            result = dato * 0.45359265
            return round(result ,2)
        
    def velocity( dato,tipo,original):
        # kh/h a...
        if str(original).lower() == "km/h":
            
            if str(tipo).lower() == "mi/h":
                result = dato * 1.60934
                return round(result ,2)
        
        
            elif str(tipo).lower() =="m/s":
                result = dato * 0.2777777777777778
                return round(result ,2) 
        # mi/h a ....
        elif str(original).lower() == "mi/h":
            
            if str(tipo).lower() == "km/h":
                result = dato * 0.621371
                return round(result ,2) 
            
            elif str(tipo).lower() =="m/s":
                result= (dato * 1.60934) *  0.2777777777777778
                return round(result ,2) 
        # m/s a ...
        elif str(original).lower() == "m/s":
            
            if str(tipo).lower() == "km/h":
                result = dato / 0.2777777777777778
                return round(result ,2) 

                
            elif str(tipo).lower() == "mi/h":
                result = (dato * 0.621371) /  0.2777777777777778
                return round(result ,2) 
            
            elif str(tipo).lower() == "ft/s":
                result = dato * 3.28084
                return round(result ,2)
        

                
                
    def distance(dato, tipo, original):
        # km a..
        if str(original).lower() == "km":

            if str(tipo).lower() == "mi":
                result = dato * 1.60934
                return round(result ,2)      
        
            elif str(tipo).lower() =="m":
                result = dato * 1000
                return round(result ,2)
                
            
            elif str(tipo).lower() =="yd":
                result = dato * 1093.61
                return round(result ,2)
                
            elif str(tipo).lower() =="in":
                result = dato * 39370.1
                return round(result ,2)
            
            elif str(tipo).lower() =="ft":
                result = dato * 3280.84
                return round(result ,2)            
        
        # metros a...
        elif str(original).lower() == "m":
            
            if str(tipo).lower() == "mi":
                result = dato * 0.000621371
                return round(result ,2)      
        
            elif str(tipo).lower() == "km":
                result = dato / 1000
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "yd":
                result = dato * 1.09361
                return round(result ,2)
            
        
        
        
            elif str(tipo).lower() =="in":
                result = dato * 39.3701
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "ft":
                result = dato * 3.28084
                return round(result ,2)
        # millas 
        elif str(original).lower() == "mi":
            
            if str(tipo).lower() == "m":
                result = dato * 1609,34
                return round(result ,2)      
        
            elif str(tipo).lower() == "km":
                result = dato * 1.60934
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "yd":
                result = dato * 1760
                return round(result ,2)
            
        
        
        
            elif str(tipo).lower() =="in":
                result = dato * 63360
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "ft":
                result = dato * 5280
                return round(result ,2)
        
        # yd 
        elif str(original).lower() == "yd":
            
            if str(tipo).lower() == "m":
                result = dato * 0.9144
                return round(result ,2)      
        
            elif str(tipo).lower() == "km":
                result = dato * 0.0009144
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "mi":
                result = dato * 0.000568182
                return round(result ,2)
            
        
        
        
            elif str(tipo).lower() =="in":
                result = dato * 36
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "ft":
                result = dato * 3
                return round(result ,2)
          # in 
        elif str(original).lower() == "in":
            
            if str(tipo).lower() == "m":
                result = dato * 0.0254
                return round(result ,2)      
        
            elif str(tipo).lower() == "km":
                result = dato * 2.54e-5
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "mi":
                result = dato * 1.5783e-5
                return round(result ,2)
            
        
                
            elif str(tipo).lower() =="yd":
                result = dato * 0.02777808
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "ft":
                result = dato * 0.08333424
                return round(result ,2)
          # ft 
        elif str(original).lower() == "ft":
            
            if str(tipo).lower() == "m":
                result = dato * 0.3048
                return round(result ,2)      
        
            elif str(tipo).lower() == "km":
                result = dato * 0.0003048
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "mi":
                result = dato * 0.000189394
                return round(result ,2)
            
        
        
        
            elif str(tipo).lower() =="yd":
                result = dato * 0.333333
                return round(result ,2)
        
        
        
            elif str(tipo).lower() == "in":
                result = dato * 12
                return round(result ,2)
            
    def height(dato, tipo, original):
        # pulgadas a
        if str(original).lower() == "in":
            
            if str(tipo).lower() =="m":
                result = dato * 0.0254
                return round(result ,2)           

            elif str(tipo).lower() =="cm":
                result = dato * 2.54
                return round(result ,2) 

            elif str(tipo).lower() == "ft":
                result = dato * 0.0833333
                return round(result ,2) 
        # metros a 
        if str(original).lower() == "m":
            
            if str(tipo).lower() =="in":
                result = dato * 39.3701
                return round(result ,2)           

            elif str(tipo).lower() =="cm":
                result = dato * 100
                return round(result ,2) 

            elif str(tipo).lower() == "ft":
                result = dato * 3.28084
                return round(result ,2)
        # centimetros a 
        if str(original).lower() == "cm":
            
            if str(tipo).lower() =="in":
                result = dato * 0.393701
                return round(result ,2)           

            elif str(tipo).lower() =="m":
                result = dato * 0.01
                return round(result ,2) 

            elif str(tipo).lower() == "ft":
                result = dato * 0.0328084
                return round(result ,2)
        # pies a 
        if str(original).lower() == "ft":
            
            if str(tipo).lower() =="in":
                result = dato * 12
                return round(result ,2)           

            elif str(tipo).lower() =="m":
                result = dato * 0.3048
                return round(result ,2) 

            elif str(tipo).lower() == "cm":
                result = dato * 30.48
                return round(result ,2) 
            
            
        
            
        
     