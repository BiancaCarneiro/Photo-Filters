import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox
import sys

image = "pictures\pic3.jpg"
img = cv2.imread(image)
r = g = b = 0
clicked = False
const_button_original = 1
const_button_gray = 2
const_button_sketch = 3
const_button_color = 4
curr_button = 0

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

class LoginForm(QWidget):
    # Defines the structure of the app
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Photo filters')
        self.resize(300, 120)

        layout = QGridLayout()
        label_name = QLabel('<font size="4"> What do you want? </font>')
        layout.addWidget(label_name, 0, 0)

        # First Button: get original picture
        button_cam = QPushButton('Camera')
        button_cam.clicked.connect(self.check_color)
        layout.addWidget(button_cam, 1, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)
        
        # Second Button: get gray picture
        button_no_cam = QPushButton('No camera')
        button_no_cam.clicked.connect(self.no_cam)
        layout.addWidget(button_no_cam, 2, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        self.setLayout(layout)

    def no_cam(self):
        self.setWindowTitle('Photo filters')
        self.resize(300, 120)

        layout = QGridLayout()
        label_name = QLabel('<font size="4"> What do you want? </font>')
        layout.addWidget(label_name, 0, 0)

        # First Button: get original picture
        button_original = QPushButton('Original')
        button_original.clicked.connect(self.show_original)
        layout.addWidget(button_original, 1, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)
        
        # Second Button: get gray picture
        button_gray = QPushButton('To gray')
        button_gray.clicked.connect(self.to_gray)
        layout.addWidget(button_gray, 2, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        
        # Third Button: get sketch picture
        button_sketch = QPushButton('To sketch')
        button_sketch.clicked.connect(self.to_sketch)
        layout.addWidget(button_sketch, 3, 0, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        # Fourth Button: check color
        button_color = QPushButton('Check color')
        button_color.clicked.connect(self.check_color)
        layout.addWidget(button_color, 3, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        self.setLayout(layout)
    def show_original(self):
        cv2.imshow("Original", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_gray(self):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Black and white", img_gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def to_sketch(self):
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
        global clicked
        msg = QMessageBox()
        cv2.namedWindow('Check Color')
        cv2.setMouseCallback('Check Color', draw_function)
        while 1:
            cv2.imshow("Check Color", img)
            if clicked:
                print("color: rgb(" + str(r) + "," + str(g) + "," + str(b) + ");")

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec_())