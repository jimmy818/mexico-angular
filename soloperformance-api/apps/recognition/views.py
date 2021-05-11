from django.shortcuts import render
from apps.recognition.utils import encoding



from .BackEnd import Recognition
import numpy as np
import boto3
import json
from django.conf import settings

# download file dataset_faces
s3 = boto3.resource('s3')

obj = s3.Object(settings.AWS_STORAGE_BUCKET_NAME, 'media/dataset_faces/dataset_faces.dat')
objecto = (obj.get()["Body"].read())

objecto.decode("ascii")
obje =objecto.decode("ascii")
all_face_encodings =json.loads(obje)


# Save the list of names and the list of encodings
known_face_id = list(all_face_encodings.items())
known_face_encodings = np.array(list(all_face_encodings.values()))

# Save the list of names and the list of encodings
known_face_id = list(all_face_encodings.keys())
known_face = []
for key, values in all_face_encodings.items():
    for value in values:
        if value =="coding":
            known_face.append(values[value])

known_face_encodings = np.array(known_face)

def viewImage(request): 

    id_user = Recognition.feace_recognition(known_face_encodings,known_face_id)

    return render(request, 'prueba_face.html',{"id":id_user})
