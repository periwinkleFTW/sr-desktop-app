from sys import exit as sysExit
from PySide2.QtWidgets import QApplication, QWidget, QPushButton, QCheckBox, QHBoxLayout

class Main(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Testing buttons")
        self.setGeometry(150, 150, 350, 350)

        self.UI()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.button = QPushButton("Button")

        self.checkbox = QCheckBox()

    def layouts(self):
        self.main_layout = QHBoxLayout()

        self.main_layout.addWidget(self.button)
        self.main_layout.addWidget(self.checkbox)

        self.setLayout(self.main_layout)



if __name__ == "__main__":
    MainEventThread = QApplication([])

    MainApplication = Main()
    MainApplication.show()

    sysExit(MainEventThread.exec_())