# python main.py
######################################################
# main.py
# This is a main script for the application
######################################################

try:
    from PySide2.QtGui     import QIcon
    from PySide2.QtWidgets import QApplication, QMainWindow, QAction

except ImportError:
    from PyQt5.QtGui     import QIcon
    from PyQt5.QtWidgets import QApplication, QMainWindow, QAction

from sys import exit as sysExit
from center_pane import CenterPanel
from backend     import Database




class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowTitle("SR test")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(150, 150, 1470, 750)

        self.setStyleSheet('QMainWindow{background-color: #F4F7F9;}')

        self.SmpRptDbase = Database("sr-data.db")

        self.CenterPane = CenterPanel(self)
        self.setCentralWidget(self.CenterPane)

        # self.MenuBar = MenuToolBar(self)

        self.StatBar = self.statusBar()
        self.SetStatusBar()

    def SetStatusBar(self, StatusMsg=''):
        if len(StatusMsg) < 1:
            StatusMsg = 'Ready'
        self.StatBar.showMessage(StatusMsg)


if __name__ == "__main__":
    MainEventThread = QApplication([])

    MainApplication = Main()
    MainApplication.show()

    sysExit(MainEventThread.exec_())
