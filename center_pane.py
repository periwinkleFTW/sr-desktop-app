######################################################
# center_pane.py
# This script contains GUI elements of the app
######################################################


from PySide2.QtWidgets import QWidget, QTabWidget, QVBoxLayout, QLabel
from PySide2.QtGui import QPixmap


from Tab_Issues import IssuesTab
from Tab_People import PeopleTab
from Tab_Facility import FacilityTab

import styles

class CenterPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.img = QPixmap('assets/logo/logo-full-main.png')
        self.logoImg = QLabel()
        self.logoImg.setPixmap(self.img)
        self.logoImg.setStyleSheet('QLabel{margin-left: 25px; margin-bottom: 25px; margin-top: 20px;}')

        self.setStyleSheet(styles.mainStyle())

        self.tbIssue = IssuesTab(self)
        self.tbPeople = PeopleTab(self)
        self.tbFclty = FacilityTab(self)

        self.TabHldr = QTabWidget()
        self.TabHldr.addTab(self.tbIssue, self.tbIssue.Title)
        self.TabHldr.addTab(self.tbPeople, self.tbPeople.Title)
        self.TabHldr.addTab(self.tbFclty, self.tbFclty.Title)

        VBox = QVBoxLayout()
        VBox.addWidget(self.logoImg)
        VBox.addWidget(self.TabHldr)

        self.setLayout(VBox)
