import cv2
import numpy as np
from keras.models import load_model

model = load_model('Model/Ex_2.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
Age = ['1-2', '3-9', '10-20', '21-27', '28-45', '46-65', '66-116']
cam = cv2.VideoCapture(0)

while True:
    ret, frame = cam.read()
    if ret:
        faces = face_cascade.detectMultiScale(frame, 1.3, 5)
        for x, y, w, h in faces:
            face = frame[y:y + h, x:x + w]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            face = cv2.resize(face, (200, 200))
            face = face.reshape(1, 200, 200, 1)
            age = model.predict(face)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            print(Age[np.argmax(age)])
            cv2.putText(frame, Age[np.argmax(age)], (x + 65, y + h + 35), cv2.FONT_HERSHEY_DUPLEX, 0.8,
                        (255, 255, 255), 2)

        cv2.imshow('Live', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()
