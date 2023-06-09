import cv2
import numpy as np
from keras.models import load_model

# model = load_model('Model/Ex_2.h5')
model = load_model('Model/model.h5')
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
Age = ['1-2', '3-6', '7-12', '13-20', '21-40', '41-60', '61-80', '81-116']

# Đường dẫn đến ảnh của bạn
image_path = 'Image/11.jpg'

# Đọc ảnh
image = cv2.imread(image_path)

# Phát hiện khuôn mặt trong ảnh
faces = face_cascade.detectMultiScale(image, 1.3, 5)

for x, y, w, h in faces:
    face = image[y:y + h, x:x + w]
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    face = cv2.resize(face, (200, 200))
    face = face.reshape(1, 200, 200, 1)
    age = model.predict(face)
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(Age[np.argmax(age)])
    cv2.putText(image, Age[np.argmax(age)], (x + 65, y + h + 35), cv2.FONT_HERSHEY_DUPLEX, 0.8,
                (255, 155, 25), 2)

# Hiển thị ảnh kết quả
cv2.imshow('Result', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
