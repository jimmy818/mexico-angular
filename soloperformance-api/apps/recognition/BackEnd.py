import cv2
import numpy as np

import face_recognition


class Recognition ():
    def feace_recognition(known_face_encodings2,known_face_names2):
        # Get a reference to webcam #0 (the default one)
        video_capture = cv2.VideoCapture(0)
        ret, frame = video_capture.read()
        # Initialize some variables
        face_locations = []
        face_encodings = []
        face_names = []
        solucion = {}
        process_this_frame = True
        i = 0
        while True:

            # Grab a single frame of video
            ret, frame = video_capture.read()
            # Resize frame of video to 1/4 size for faster face recognition processing
            try:
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Only process every other frame of video to save time
                if process_this_frame:
                    # Find all the faces and face encodings in the current frame of video
                    face_locations = face_recognition.face_locations(rgb_small_frame)
                    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

                    face_names = []
                    for face_encoding in face_encodings:
                        # See if the face is a match for the known face(s)
                        matches = face_recognition.compare_faces(known_face_encodings2, face_encoding)

                    

                        # Or instead, use the known face with the smallest distance to the new face
                        face_distances = face_recognition.face_distance(known_face_encodings2, face_encoding)
                        best_match_index = np.argmin(face_distances)
                        if matches[best_match_index]:
                            name = known_face_names2[best_match_index]
                            #variable to update dic
                            if  name not in solucion.keys():
                                result = {name : 0}
                                solucion.update( result)


                            # Obtein the ame of person
                            face_names.append(name)


                process_this_frame = not process_this_frame


                # Display the results
                for (top, right, bottom, left), name in zip(face_locations, face_names):       
                
                    result2 = {name:(solucion[name]+1)}
                    solucion.update(result2)
                    
                # Display the resulting image
                #cv2.imshow('Video', frame)


                for key , value in solucion.items():
                    #print(f"{key}--< key , {value}-->Valor ")
                    if  cv2.waitKey(1) & value == 20:
                        retornar = key
                        video_capture.release()
                        cv2.destroyAllWindows() 
                                    
                        return retornar
            except:
                return "Webcam does not work "
