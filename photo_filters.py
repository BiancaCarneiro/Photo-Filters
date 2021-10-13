from PyQt5.QtGui import QIcon
import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QGridLayout, QMessageBox
import sys


image = "pictures\pic3.jpg"
img = cv2.imread(image)
r = g = b = 0
clicked = False

def exit_app():
    app.quit()

def draw_function(event, x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global b, g, r, clicked
        clicked = True
        b,g,r = img[y,x]
        b = int(b)
        g = int(g)
        r = int(r)

class PhotoFilters(QWidget):
    # Defines the structure of the app
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Photo filters')
        self.resize(300, 120)
        self.setWindowIcon(QIcon("pictures/PFlogo.png"))

        layout = QGridLayout()
        label_name = QLabel('<font size="4"> What do you want? </font>')
        layout.addWidget(label_name, 0, 0)

        button_original = QPushButton('Original')
        button_original.clicked.connect(self.show_original)
        layout.addWidget(button_original, 1, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_camera = QPushButton('Camera')
        button_camera.clicked.connect(self.open_camera)
        layout.addWidget(button_camera, 1, 0, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_toGray = QPushButton('To gray')
        button_toGray.clicked.connect(self.to_gray)
        layout.addWidget(button_toGray, 2, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_toGrayCam = QPushButton('To gray camera')
        button_toGrayCam.clicked.connect(self.to_gray_camera)
        layout.addWidget(button_toGrayCam, 2, 0, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_sketch = QPushButton('To sketch')
        button_sketch.clicked.connect(self.to_sketch)
        layout.addWidget(button_sketch, 3, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_sketchCam = QPushButton('To sketch camera')
        button_sketchCam.clicked.connect(self.to_sketch_camera)
        layout.addWidget(button_sketchCam, 3, 0, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_CheckColor = QPushButton('Check color')
        button_CheckColor.clicked.connect(self.check_color)
        layout.addWidget(button_CheckColor, 4, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_CheckColorCam = QPushButton('Check color camera')
        button_CheckColorCam.clicked.connect(self.check_color_camera)
        layout.addWidget(button_CheckColorCam, 4, 0, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        self.setLayout(layout)

    def open_camera(self):
        #print("camera")
        cam = cv2.VideoCapture(0)
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Press space to save the picture and ESC to leave", frame)
            k = cv2.waitKey(1)
            if k%256 == 27:
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "original_pic_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame)
                img_counter += 1
        cam.release()
        cv2.destroyAllWindows()

    def to_gray_camera(self):
        cam = cv2.VideoCapture(0)
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            cv2.imshow("Press space to save the picture and ESC to leave", frame_gray)
            k = cv2.waitKey(1)
            if k%256 == 27:
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "gray_pic_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame_gray)
                img_counter += 1
        cam.release()
        cv2.destroyAllWindows()

    def to_sketch_camera(self):
        cam = cv2.VideoCapture(0)
        img_counter = 0
        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            # lets create a sketch
            # Steps:
            # 1: Convert to grey -> DONE
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 2: Invert Image
            frame_invert = cv2.bitwise_not(frame_gray)
            # 3: Blur image
            frame_blur = cv2.GaussianBlur(frame_invert, (111,111),0)
            # 4: Invert Blurred image
            frame_blurinvert = cv2.bitwise_not(frame_blur)
            # 5: bit-wise division -> Final step
            frame_sketch = cv2.divide(frame_gray, frame_blurinvert, scale=256.0)
            cv2.imshow("Press space to save the picture and ESC to leave", frame_sketch)
            k = cv2.waitKey(1)
            if k%256 == 27:
                break
            elif k%256 == 32:
                # SPACE pressed
                img_name = "sketch_pic_{}.png".format(img_counter)
                cv2.imwrite(img_name, frame_sketch)
                img_counter += 1
        cam.release()
        cv2.destroyAllWindows()

    def check_color_camera(self):
        global clicked
        global img
        msg = QMessageBox()
        cam = cv2.VideoCapture(0)
        cv2.namedWindow('Check Color - Press ESC to leave')
        cv2.setMouseCallback('Check Color - Press ESC to leave', draw_function)
        while True:
            ret, img = cam.read()
            cv2.imshow("Check Color - Press ESC to leave", img)
            if clicked:
                #print("color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ");")

                msg.setText("R: " + str(r) + "   G: " + str(g) + "   B: " + str(b))
                if r+g+b < 300:
                    msg.setStyleSheet("color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ");")
                else:
                    msg.setStyleSheet("QMessageBox{background-color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ")}")
                msg.exec_()
                clicked = False
            if cv2.waitKey(20) & 0xFF ==27:
                break
        cam.release()
        cv2.destroyAllWindows()

    def show_original(self):
        global img
        img = cv2.imread(image)
        cv2.imshow("Original", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_gray(self):
        global img
        img = cv2.imread(image)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Black and white", img_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_sketch(self):
        global img
        img = cv2.imread(image)
        # lets create a sketch
        # Steps:
        # 1: Convert to grey -> DONE
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # 2: Invert Image
        img_invert = cv2.bitwise_not(img_gray)
        # 3: Blur image
        img_blur = cv2.GaussianBlur(img_invert, (111,111),0)
        # 4: Invert Blurred image
        img_blurinvert = cv2.bitwise_not(img_blur)
        # 5: bit-wise division -> Final step
        img_sketch = cv2.divide(img_gray, img_blurinvert, scale=256.0)
        cv2.imshow("Sketch", img_sketch)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def check_color(self):
        global img
        img = cv2.imread(image)
        global clicked
        msg = QMessageBox()
        cv2.namedWindow('Check Color - Press ESC to leave')
        cv2.setMouseCallback('Check Color - Press ESC to leave', draw_function)
        while 1:
            cv2.imshow("Check Color - Press ESC to leave", img)
            if clicked:
                #print("color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ");")

                msg.setText("R: " + str(r) + "   G: " + str(g) + "   B: " + str(b))
                if r+g+b < 300:
                    msg.setStyleSheet("color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ");")
                else:
                    msg.setStyleSheet("QMessageBox{background-color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ")}")
                msg.exec_()
                clicked = False
            # EXITS WITH ESC + X
            if cv2.waitKey(20) & 0xFF ==27:
                break
        cv2.destroyAllWindows()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = PhotoFilters()
    form.show()
    sys.exit(app.exec_())