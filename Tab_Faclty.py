try:
   from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
   from PySide2.QtWidgets import QRadioButton, QHBoxLayout, QVBoxLayout
   from PySide2.QtWidgets import QTableWidgetItem, QTableWidget, QGroupBox
   from PySide2.QtWidgets import QHeaderView, QTableView, QAbstractItemView, QCheckBox

except ImportError:
   from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
   from PyQt5.QtWidgets import QRadioButton, QHBoxLayout, QVBoxLayout
   from PyQt5.QtWidgets import QTableWidgetItem, QTableWidget, QGroupBox
   from PyQt5.QtWidgets import QHeaderView, QTableView, QAbstractItemView, QCheckBox

from backend import Database

db = Database("sr-data.db")

class FacltyTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.FcltyTitle = 'Facilities'

        self.UI()

    @property
    def Title(self):
        return self.FcltyTitle

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Facilities widgets ###########################################################
        # Top layout (search facilities) widgets
        self.searchFacilitiesText = QLabel("Search facilities: ")
        self.searchFacilitesEntry = QLineEdit()
        self.searchFacilitesEntry.setPlaceholderText("Search facilities..")
        self.searchFacilitiesBtn = QPushButton("Search")
        # self.searchFacilitiesBtn.clicked.connect(self.searchFacilities)

        # Middle layout (list people) widgets with radio buttons
        self.allFacilitiesRadioBtn = QRadioButton("All facilities")
        self.withOngoingIssuesFacilitiesRadioBtn = QRadioButton("With ongoing issues")
        self.withLateIssuesRadioBtn = QRadioButton("With late issues")
        self.listFacilitiesBtn = QPushButton("List facilities")

        # Bottom layout widget, a table showing people
        self.facilitiesTable = QTableWidget()
        self.facilitiesTable.setColumnCount(10)
        # self.peopleTable.setColumnHidden(0, True)
        self.facilitiesTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.facilitiesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Name"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Location"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Phone"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Email"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Supervisor"))
        self.facilitiesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Ongoing issues"))
        self.facilitiesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Late issues"))
        self.facilitiesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Total issues"))
        self.facilitiesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Total inspections"))

        # Double clicking a row opens a window with person details
        # self.facilitiesTable.doubleClicked.connect(self.selectedFacility)

        # Buttons for actions on selected facilities
        self.refreshFacilitiesBtn = QPushButton("Refresh")
        # self.refreshFacilitiesBtn.clicked.connect(self.displayFacilities)
        self.addFacility = QPushButton("Add facility")
        # self.addFacility.clicked.connect(self.funcAddFacility)
        self.viewFacility = QPushButton("View/Edit facility")
        # self.viewFacility.clicked.connect(self.selectedFacility)
        self.deleteFacility = QPushButton("Delete facility")
        # self.deleteFacility.clicked.connect(self.funcDeleteFacility)
        self.exportFacilitiesCSVBtn = QPushButton("Export CSV")
        # self.exportFacilitiesCSVBtn.clicked.connect(self.funcFacilitiesToCSV)
        self.exportFacilitiesXSLXBtn = QPushButton("Export XLSX")
        # self.exportFacilitiesXSLXBtn.clicked.connect(self.funcFacilitiesToXLSX)


    def layouts(self):
        # Facilities layouts ###########################################################
        self.facilitiesMainLayout = QVBoxLayout()
        self.facilitiesMainTopLayout = QHBoxLayout()
        self.facilitiesMainMiddleLayout = QHBoxLayout()
        self.facilitiesMainBottomLayout = QHBoxLayout()
        self.facilitiesBottomRightLayout = QVBoxLayout()
        self.facilitiesBottomLeftLayout = QHBoxLayout()
        # Groupboxes allows customization using CSS-like syntax
        self.facilitiesTopGroupBox = QGroupBox("Search Box")
        self.facilitiesTopGroupBoxRightFiller = QGroupBox()
        self.facilitiesMiddleGroupBox = QGroupBox("List Box")
        self.facilitiesMiddleGroupBoxRightFiller = QGroupBox()
        self.facilitiesBottomGroupBox = QGroupBox()
        self.facilitiesBottomLeftGroupBox = QGroupBox("Facilities")
        self.facilitiesBottomRightGroupBox = QGroupBox("Actions")
        self.facilitiesBottomRightGroupBoxFiller = QGroupBox()

        # Top layout (search box) widgets
        self.facilitiesMainTopLayout.addWidget(self.searchFacilitiesText, 10)
        self.facilitiesMainTopLayout.addWidget(self.searchFacilitesEntry, 30)
        self.facilitiesMainTopLayout.addWidget(self.searchFacilitiesBtn, 10)
        self.facilitiesMainTopLayout.addWidget(self.facilitiesTopGroupBoxRightFiller, 50)
        self.facilitiesTopGroupBox.setLayout(self.facilitiesMainTopLayout)

        # Middle layout (list box) widgets
        self.facilitiesMainMiddleLayout.addWidget(self.allFacilitiesRadioBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.withOngoingIssuesFacilitiesRadioBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.withLateIssuesRadioBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.listFacilitiesBtn)
        self.facilitiesMainMiddleLayout.addWidget(self.facilitiesMiddleGroupBoxRightFiller, 65)
        self.facilitiesMiddleGroupBox.setLayout(self.facilitiesMainMiddleLayout)

        # Bottom layout (table with facilities) widgets
        # Bottom left layout with table
        self.facilitiesBottomLeftLayout.addWidget(self.facilitiesTable)
        self.facilitiesBottomLeftGroupBox.setLayout(self.facilitiesBottomLeftLayout)

        # Bottom right layout with buttons
        self.facilitiesBottomRightLayout.addWidget(self.refreshFacilitiesBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.addFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.viewFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.deleteFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.facilitiesBottomRightGroupBoxFiller, 70)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesCSVBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesXSLXBtn, 5)
        self.facilitiesBottomRightGroupBox.setLayout(self.facilitiesBottomRightLayout)

        self.facilitiesMainBottomLayout.addWidget(self.facilitiesBottomLeftGroupBox, 90)
        self.facilitiesMainBottomLayout.addWidget(self.facilitiesBottomRightGroupBox, 10)

        self.facilitiesMainLayout.addWidget(self.facilitiesTopGroupBox, 10)
        self.facilitiesMainLayout.addWidget(self.facilitiesMiddleGroupBox, 10)
        self.facilitiesMainLayout.addLayout(self.facilitiesMainBottomLayout, 80)

        self.setLayout(self.facilitiesMainLayout)

