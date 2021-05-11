
import boto3
import numpy as np
import face_recognition
import json
import tempfile    
from django.conf import settings
def encoding(data):
    
    # open the data
  
    s3 = boto3.resource('s3')
    obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'media/dataset_faces/dataset_faces.dat')
    objecto = (obj.get()["Body"].read())

  
    
    obje =objecto.decode("ascii")
    all_face_encodings = json.loads(obje)
    if data.photo:
        
    
            if str(data.id) not in list(all_face_encodings.keys()):
                
                try:
                    image = face_recognition.load_image_file(data.photo)               
                    all_face_encodings[data.id] = {"coding": face_recognition.face_encodings(image)[0],
                                                   "url":   str(data.photo)}
                    #Created temp file,
                    outfile = tempfile.NamedTemporaryFile(suffix=".dat")  
                    encodes = json.dumps(all_face_encodings, cls=NumpyArrayEncoder)
                    # write file
                    outfile.write(encodes.encode("ascii"))
                    s3 = boto3.resource('s3')
                    #send file
                    s3.meta.client.upload_file(outfile.name, settings.AWS_STORAGE_BUCKET_NAME, 'media/dataset_faces/dataset_faces.dat')
                    #close temp file
                    outfile.close()
                    return "Save ",data.id

                except  IndexError as error:

                    return "The photo does not contain or does not recognize your face, please enter another photo"
                
            elif str(data.id)  in list(all_face_encodings.keys()) and str(data.photo) != str(all_face_encodings[str(data.id)]["url"]) : 
                try:
                    image = face_recognition.load_image_file(data.photo)               
                    all_face_encodings[data.id] = {"coding": face_recognition.face_encodings(image)[0],
                                                   "url":   str(data.photo)}
                    #Created temp file,
                    outfile = tempfile.NamedTemporaryFile(suffix=".dat")  
                    encodes = json.dumps(all_face_encodings, cls=NumpyArrayEncoder)
                    # write file
                    outfile.write(encodes.encode("ascii"))
                    s3 = boto3.resource('s3')
                    #send file
                    s3.meta.client.upload_file(outfile.name, settings.AWS_STORAGE_BUCKET_NAME, 'media/dataset_faces/dataset_faces.dat')
                    #close temp file
                    outfile.close()
                    return "Updated",data.id
                
                except  IndexError as error:

                    return "The photo does not contain or does not recognize your face, please enter another photo"
            
            else:
                return ("User already are register")

    s3 = boto3.resource('s3') 
    obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'media/dataset_faces/dataset_faces.dat')
    objecto = (obj.get()["Body"].read())

  
    objecto.decode("ascii")
    obje =objecto.decode("ascii")
    all_face_encodings =json.loads(obje)
    if data.photo:       
        if data.id not in all_face_encodings[True][0].keys():
            
            try:
                
                image = face_recognition.load_image_file(data.photo)               
                all_face_encodings[data.id] = face_recognition.face_encodings(image)[0]
                #Created temp file,
                outfile = tempfile.NamedTemporaryFile(suffix=".dat")  
                encodes = json.dumps(all_face_encodings, cls=NumpyArrayEncoder)
                # write file
                outfile.write(encodes.encode("ascii"))
                #send file
                s3.meta.client.upload_file(outfile.name, settings.AWS_STORAGE_BUCKET_NAME, 'media/dataset_faces/dataset_faces.dat')
                #close temp file
                outfile.close()
                return 

            except  IndexError as error:
                print( "The photo does not contain or does not recognize your face, please enter another photo")

                return "The photo does not contain or does not recognize your face, please enter another photo"
        else: print("User already are register")
    else:
        return "User without photo"
   
    
class NumpyArrayEncoder(json.JSONEncoder):
                    def default(self, obj):
                        if isinstance(obj, np.ndarray):
                            return obj.tolist()
                        return json.JSONEncoder.default(self, obj)
