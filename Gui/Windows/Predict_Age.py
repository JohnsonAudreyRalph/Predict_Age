import cv2
import numpy as np
import re
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QFileDialog
from PyQt5.uic import loadUi
from keras.models import load_model
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", message="AutoGraph.*")


model = load_model('Model/model.h5')
Age = ['1-2', '3-6', '7-12', '13-20', '21-40', '41-60', '61-80', '81-116']
face_cascade = cv2.CascadeClassifier('Model/haarcascade_frontalface_default.xml')
file_path = "ID_Cameras.txt"


def Predict_Age_Camera(frame):
    faces = face_cascade.detectMultiScale(frame, 1.3, 5)
    for x, y, w, h in faces:
        face = frame[y:y + h, x:x + w]
        face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        face = cv2.resize(face, (200, 200))
        face = face.reshape(1, 200, 200, 1)
        age = model.predict(face)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # print("===>", Age[np.argmax(age)])
        cv2.putText(frame, Age[np.argmax(age)], (x + 65, y + h + 35), cv2.FONT_HERSHEY_DUPLEX, 0.8,
                    (255, 255, 255), 2)
    return frame


def is_numeric_string(string):
    for char in string:
        if not char.isdigit():
            return False
    return True


def contains_ip_pattern(string):
    pattern = r"192\.168\.\d+\.\d+"
    if re.search(pattern, string):
        return True
    return False


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.is_webcam_on = None
        self.capture = None
        self.ui_files = {
            'Gui_Start': {'file': 'File_UI/Gui_Start.ui', 'width': 1130, 'height': 605},
            'Gui_Camera': {'file': 'File_UI/Gui_Camera.ui', 'width': 1130, 'height': 605},
            'Gui_Image': {'file': 'File_UI/Gui_Image.ui', 'width': 1130, 'height': 605},
            'Gui_Change_Camera': {'file': 'File_UI/Gui_Change_Camera.ui', 'width': 772, 'height': 150},
            'Gui_Auther': {'file': 'File_UI/Gui_Auther.ui', 'width': 835, 'height': 330},
        }
        self.load_ui('Gui_Start')
        self.actionCamera.triggered.connect(self.Camera)
        self.actionImage.triggered.connect(self.Image)
        self.actionChange_Camera.triggered.connect(self.Change_Camera)
        self.actionAuthor.triggered.connect(self.Author)
        self.is_webcam_on = False

    def load_ui(self, ui_name):
        ui_info = self.ui_files.get(ui_name)
        if ui_info:
            file_paths = ui_info['file']
            width = ui_info['width']
            height = ui_info['height']
            # Load giao diện từ file .ui
            loadUi(file_paths, self)
            # Đặt kích thước cố định cho cửa sổ chương trình
            self.setFixedSize(width, height)

    def closeEvent(self, event):
        reply = QMessageBox.question(self, "Xác nhận thoát", "Bạn có chắc chắn muốn thoát?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.is_webcam_on = False
            # print("Bạn đã thoát")
            event.accept()
            self.close()  # Close the window
        else:
            event.ignore()

    def Start_Camera(self):
        with open(file_path, "r") as file:
            ID_Camera = file.read()
        # print("Đã đọc giá trị ID_Camera từ file ID_Cameras.txt:", ID_Camera)
        # ID_Camera chỉ chứa các chữ số từ 0 đến 9
        if is_numeric_string(ID_Camera):
            self.capture = cv2.VideoCapture(int(ID_Camera))
        # ID_Camera có tồn tại địa chỉ IP --> Đây là IP của Camera Wifi
        if contains_ip_pattern(ID_Camera):
            # print("Đã tìm thấy, trong ID_Camera vừa nhập có giá trị: 192.168.x.x")
            self.capture = cv2.VideoCapture(str(ID_Camera))
        self.is_webcam_on = True
        self.is_webcam_on = self.capture.isOpened()
        if self.is_webcam_on:
            while self.is_webcam_on:
                ret, frame = self.capture.read()
                if ret:
                    frame = Predict_Age_Camera(frame)
                    frame = cv2.resize(frame, [1120, 820])
                    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    image = QImage(image, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
                    pixmap = QPixmap.fromImage(image)
                    self.Show_Camera.setPixmap(pixmap)
                    QApplication.processEvents()
            self.capture.release()
        else:
            QMessageBox.information(self, "Lỗi", "Chưa kết nối với Camera", QMessageBox.Ok)

    def Start_Image(self):
        # print("Bạn đã bấm nút")
        file_dialog = QFileDialog()
        file_dialog.setFileMode(QFileDialog.ExistingFile)
        file_dialog.setNameFilter("Images (*.png *.xpm *.jpg *.bmp)")
        if file_dialog.exec_():
            selected_files = file_dialog.selectedFiles()
            image_path = selected_files[0]
            image = cv2.imread(image_path)
            faces = face_cascade.detectMultiScale(image, 1.3, 5)
            for x, y, w, h in faces:
                face = image[y:y + h, x:x + w]
                face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
                face = cv2.resize(face, (200, 200))
                face = face.reshape(1, 200, 200, 1)
                age = model.predict(face)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(image, Age[np.argmax(age)], (x + 65, y + h + 35), cv2.FONT_HERSHEY_DUPLEX, 0.8,
                            (255, 155, 25), 2)
            # Chuyển đổi màu ảnh từ BGR sang RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # Tạo đối tượng QImage từ mảng numpy của ảnh
            qimage = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qimage)
            self.Show_Image.setPixmap(pixmap)
            self.Show_Image.setScaledContents(True)

    def Change_ID_Camera(self):
        # print("Xác nhận bạn đã nhấn nút thay đổi ID Camera!")
        ID_Camera = self.ID_Camera.toPlainText()
        # print(ID_Camera)
        with open(file_path, "w") as file:
            file.write(ID_Camera)
        # print(f"Đã lưu giá trị {ID_Camera} vào file ID_Cameras.txt")

    def Camera(self):
        # print("Đã gọi đến camera")
        self.load_ui('Gui_Camera')
        self.actionImage.triggered.connect(self.Image)
        self.actionChange_Camera.triggered.connect(self.Change_Camera)
        self.actionAuthor.triggered.connect(self.Author)
        self.Start.clicked.connect(self.Start_Camera)

    def Image(self):
        # print("Đã gọi đến Image")
        self.is_webcam_on = False
        self.load_ui('Gui_Image')
        self.actionCamera.triggered.connect(self.Camera)
        self.actionChange_Camera.triggered.connect(self.Change_Camera)
        self.actionAuthor.triggered.connect(self.Author)
        self.btn_Search.clicked.connect(self.Start_Image)

    def Change_Camera(self):
        # print("Đã gọi đến thay đổi Camera")
        self.is_webcam_on = False
        self.load_ui('Gui_Change_Camera')
        self.actionCamera.triggered.connect(self.Camera)
        self.actionImage.triggered.connect(self.Image)
        self.actionAuthor.triggered.connect(self.Author)
        with open(file_path, "r") as file:
            ID_Camera = file.read()
            self.ID_Camera.setPlainText(ID_Camera)
        self.btn_Change_ID.clicked.connect(self.Change_ID_Camera)

    def Author(self):
        # print("Đã gọi đến Author")
        self.is_webcam_on = False
        self.load_ui('Gui_Auther')
        self.actionCamera.triggered.connect(self.Camera)
        self.actionImage.triggered.connect(self.Image)
        self.actionChange_Camera.triggered.connect(self.Change_Camera)


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = MainWindow()
    window.setWindowTitle("Dự đoán tuổi qua khuôn mặt")
    window.show()
    app.exec()
