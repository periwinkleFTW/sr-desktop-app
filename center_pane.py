######################################################
# center_pane.py
# This script contains GUI elements of the app
######################################################

try:
    from PySide2.QtWidgets import QWidget, QTabWidget, QHBoxLayout

except ImportError:
    from PyQt5.QtWidgets import QWidget, QTabWidget, QHBoxLayout

# Note the following are not part of PySide2 nor PyQt5 so not need to put within this
# structure -- btw why do you keep duplicating PySide2 within the Try and Except that 
# is totally pointless

# I name the files like this so they are sorted next to one another within the folder
# I keep name lengths for like things as close to one another for clarity when they are
# grouped as you can see how this looks when done this way
from Tab_Issues import IssuesTab
from Tab_People import PeopleTab
from Tab_Faclty import FacltyTab

class CenterPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

#        self.tbFclty = FacltyTab(self)
        self.tbIssue = IssuesTab(self)
#        self.tbPeple = PeopleTab(self)

        self.TabHldr = QTabWidget()
        self.TabHldr.addTab(self.tbIssue, self.tbIssue.Title)
#        self.TabHldr.addTab(self.tbPeple, self.tbPeple.Title)
#        self.TabHldr.addTab(self.tbFclty, self.tbFclty.Title)

        HBox = QHBoxLayout()
        HBox.addWidget(self.TabHldr)

        self.setLayout(HBox)
