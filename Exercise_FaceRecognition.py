# pip install mediapipe face_recognition opencv-python numpy
# 
# python --version
# Python 3.10.17
#

import cv2
import mediapipe as mp
import face_recognition
import numpy as np
import pickle

# Initialize Mediapipe Face Detection
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

# Initialize webcam
cap = cv2.VideoCapture(0)

# Data for known faces (face encodings and names)
known_face_encodings = []
known_face_names = []

# Load saved faces and names (if available)
try:
    with open("known_faces.pkl", "rb") as f:
        known_face_encodings, known_face_names = pickle.load(f)
except FileNotFoundError:
    pass

with mp_face_detection.FaceDetection(min_detection_confidence=0.2) as face_detection:
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        
        # Convert the image to RGB (Mediapipe needs RGB)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Perform face detection (Mediapipe)
        results = face_detection.process(rgb_frame)

        face_names = []
        face_locations = []
        face_encodings = []

        # If faces are detected
        if results.detections:
            for detection in results.detections:
                # Draw the face
                mp_drawing.draw_detection(frame, detection)

                # Extract the face's position
                bboxC = detection.location_data.relative_bounding_box
                h, w, c = frame.shape
                top, left, bottom, right = int(bboxC.ymin * h), int(bboxC.xmin * w), int((bboxC.ymin + bboxC.height) * h), int((bboxC.xmin + bboxC.width) * w)
                face_locations.append((top, right, bottom, left))

                # At this point, you should extract face encodings using face_recognition
                # You will need to implement this part, where face encodings for the detected faces are extracted.
                # The encodings should be stored in `face_encodings` list.

                '''
                # Find all the faces in the image
                face_locations = face_recognition.face_locations(rgb_frame)
                print(face_locations)

                # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
                results = face_recognition.compare_faces(known_face_encodings, known_face_names)
                
                break
                '''         
               
                face_image = rgb_frame[top:bottom, left:right]
                # Get face encodings for the cropped face
                encodings = face_recognition.face_encodings(rgb_frame, [(top, right, bottom, left)])
                if len(encodings) > 0:
                    face_encodings.append(encodings[0])





            # The next step is to identify faces based on the encodings.
            # Here, you need to compare the current face encodings with the known face encodings.
            # This part can be implemented by comparing face encodings using a comparison function.
            # (see https://face-recognition.readthedocs.io/en/stable/face_recognition.html#face_recognition.api.compare_faces)
            # The identified names should be stored in `face_names`.

            for face_encoding in face_encodings:
                matches = face_recognition.api.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
                name = "Unknown"

                # Use the known face with the smallest distance to the new face
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                if len(matches) > 0:
                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = known_face_names[best_match_index]

                face_names.append(name)



        # Draw the recognized faces and their names
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (0, 0, 0), 1)

        # Display the image
        cv2.imshow('Face Detection and Recognition', frame)

        # Save a new face when 's' is pressed
        key = cv2.waitKey(1)
        if key == ord('s'):
            if len(face_encodings) > 0:
                name = input("Enter your name: ")
                known_face_encodings.append(face_encodings[0])
                known_face_names.append(name)

                with open("known_faces.pkl", "wb") as f:
                    pickle.dump((known_face_encodings, known_face_names), f)

                print(f"Face of '{name}' has been saved.")
        
        if key == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
