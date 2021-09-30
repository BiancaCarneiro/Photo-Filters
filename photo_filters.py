import cv2
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox
import sys




image = "pictures\pic3.jpg"
img = cv2.imread(image)

def exit_app():
    app.quit()

class LoginForm(QWidget):
    # Defines the structure of the app
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Photo filters')
        self.resize(300, 120)

        layout = QGridLayout()
        label_name = QLabel('<font size="4"> What do you want? </font>')
        layout.addWidget(label_name, 0, 0)

        button_login = QPushButton('Original')
        button_login.clicked.connect(self.show_original)
        layout.addWidget(button_login, 1, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_login = QPushButton('To gray')
        button_login.clicked.connect(self.to_gray)
        layout.addWidget(button_login, 2, 1, 1, 1)
        layout.setRowMinimumHeight(2, 25)

        button_signup = QPushButton('To sketch')
        button_signup.clicked.connect(self.to_sketch)
        layout.addWidget(button_signup, 3, 1, 1, 1)
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




if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = LoginForm()
    form.show()
    sys.exit(app.exec_())