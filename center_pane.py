######################################################
# center_pane.py
# This script contains GUI elements of the app
######################################################

try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QVBoxLayout
    from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QTableView
    from PySide2.QtWidgets import QGroupBox, QAbstractItemView, QFileDialog, QLabel
    from PySide2.QtWidgets import QRadioButton, QCheckBox, QLineEdit, QPushButton
    from issues_tab import IssuesTab
    from people_tab import PeopleTab
    from facilities_tab import FacilitiesTab

except ImportError:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget, QTabWidget, QHBoxLayout, QVBoxLayout
    from PySide2.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QTableView
    from PySide2.QtWidgets import QGroupBox, QAbstractItemView, QFileDialog, QLabel
    from PySide2.QtWidgets import QRadioButton, QCheckBox, QLineEdit, QPushButton
    from issues_tab import IssuesTab
    from people_tab import PeopleTab
    from facilities_tab import FacilitiesTab


class CenterPanel(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.UI()
        self.show()

    def UI(self):
        self.tabWidget()

    def tabWidget(self):
        self.tabs = QTabWidget()
        self.tab1 = IssuesTab(self)
        self.tab2 = PeopleTab(self)
        self.tab3 = FacilitiesTab(self)

        self.tabs.addTab(self.tab1, "Issues")
        self.tabs.addTab(self.tab2, "People")
        self.tabs.addTab(self.tab3, "Facilities")

        HBox = QHBoxLayout()
        HBox.addWidget(self.tabs)

        self.setLayout(HBox)
