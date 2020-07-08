
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
    QTableWidgetItem, QTableWidget, QGroupBox, QHeaderView

class PeopleTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.PeoplTitle = 'People'

        self.UI()

    @property
    def Title(self):
        return self.PeoplTitle

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # People widgets ###########################################################
        # Top layout (search people) widgets
        self.searchPeopleText = QLabel("Search people: ")
        self.searchPeopleEntry = QLineEdit()
        self.searchPeopleEntry.setPlaceholderText("Search people..")
        self.searchPeopleBtn = QPushButton("Search")
        # self.searchPeopleBtn.clicked.connect(self.searchPeople)

        # Middle layout (list people) widgets with radio buttons
        self.allPeopleRadioBtn = QRadioButton("All people")
        self.employeesPeopleRadioBtn = QRadioButton("Employees")
        self.contractorsPeopleRadioBtn = QRadioButton("Contractors")
        self.subcontractorsPeopleRadioBtn = QRadioButton("Subcontractors")
        self.listPeopleBtn = QPushButton("List people")
        # self.listPeopleBtn.clicked.connect(self.listPeople)

        # Bottom layout widget, a table showing people
        self.peopleTable = QTableWidget()
        self.peopleTable.setColumnCount(8)
        # self.peopleTable.setColumnHidden(0, True)
        self.peopleTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.peopleTable.setHorizontalHeaderItem(1, QTableWidgetItem("First name"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(2, QTableWidgetItem("Last name"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(3, QTableWidgetItem("Title"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(4, QTableWidgetItem("Phone"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(5, QTableWidgetItem("Email"))
        self.peopleTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.peopleTable.setHorizontalHeaderItem(6, QTableWidgetItem("Location"))
        self.peopleTable.setHorizontalHeaderItem(7, QTableWidgetItem("Employment type"))

        # Double clicking a row opens a window with person details
        # self.peopleTable.doubleClicked.connect(self.selectedPerson)

        # Buttons for actions on selected people
        self.refreshPeopleBtn = QPushButton("Refresh")
        # self.refreshPeopleBtn.clicked.connect(self.displayPeople)
        self.addPerson = QPushButton("Add person")
        # self.addPerson.clicked.connect(self.funcAddPerson)
        self.viewPerson = QPushButton("View/Edit person")
        # self.viewPerson.clicked.connect(self.selectedPerson)
        self.deletePerson = QPushButton("Delete person")
        # self.deletePerson.clicked.connect(self.funcDeletePerson)
        self.exportPeopleCSVBtn = QPushButton("Export CSV")
        # self.exportPeopleCSVBtn.clicked.connect(self.funcPeopleToCSV)
        self.exportPeopleXLSXBtn = QPushButton("Export XLSX")
        # self.exportPeopleXLSXBtn.clicked.connect(self.funcPeopleToXLSX)


    def layouts(self):
        # People layouts ###########################################################
        self.peopleMainLayout = QVBoxLayout()
        self.peopleMainTopLayout = QHBoxLayout()
        self.peopleMainMiddleLayout = QHBoxLayout()
        self.peopleMainBottomLayout = QHBoxLayout()
        self.peopleBottomRightLayout = QVBoxLayout()
        self.peopleBottomLeftLayout = QHBoxLayout()
        # Groupboxes allows customization using CSS-like syntax
        self.peopleTopGroupBox = QGroupBox("Search Box")
        self.peopleTopGroupBoxRightFiller = QGroupBox()
        self.peopleMiddleGroupBox = QGroupBox("List Box")
        self.peopleMiddleGroupBoxRightFiller = QGroupBox()
        self.peopleBottomGroupBox = QGroupBox()
        self.peopleBottomLeftGroupBox = QGroupBox("People")
        self.peopleBottomRightGroupBox = QGroupBox("Actions")
        self.peopleBottomRightGroupBoxFiller = QGroupBox()

        # Top layout (search box) widgets
        self.peopleMainTopLayout.addWidget(self.searchPeopleText, 10)
        self.peopleMainTopLayout.addWidget(self.searchPeopleEntry, 30)
        self.peopleMainTopLayout.addWidget(self.searchPeopleBtn, 10)
        self.peopleMainTopLayout.addWidget(self.peopleTopGroupBoxRightFiller, 50)
        self.peopleTopGroupBox.setLayout(self.peopleMainTopLayout)

        # Middle layout (list box) widgets
        self.peopleMainMiddleLayout.addWidget(self.allPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.employeesPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.contractorsPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.subcontractorsPeopleRadioBtn)
        self.peopleMainMiddleLayout.addWidget(self.listPeopleBtn)
        self.peopleMainMiddleLayout.addWidget(self.peopleMiddleGroupBoxRightFiller, 65)
        self.peopleMiddleGroupBox.setLayout(self.peopleMainMiddleLayout)

        # Bottom layout (table with issues) widgets
        # Bottom left layout with table
        self.peopleBottomLeftLayout.addWidget(self.peopleTable)
        self.peopleBottomLeftGroupBox.setLayout(self.peopleBottomLeftLayout)

        # Bottom right layout with buttons
        self.peopleBottomRightLayout.addWidget(self.refreshPeopleBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.addPerson, 5)
        self.peopleBottomRightLayout.addWidget(self.viewPerson, 5)
        self.peopleBottomRightLayout.addWidget(self.deletePerson, 5)
        self.peopleBottomRightLayout.addWidget(self.peopleBottomRightGroupBoxFiller, 70)
        self.peopleBottomRightLayout.addWidget(self.exportPeopleCSVBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.exportPeopleXLSXBtn, 5)
        self.peopleBottomRightGroupBox.setLayout(self.peopleBottomRightLayout)

        self.peopleMainBottomLayout.addWidget(self.peopleBottomLeftGroupBox, 90)
        self.peopleMainBottomLayout.addWidget(self.peopleBottomRightGroupBox, 10)

        self.peopleMainLayout.addWidget(self.peopleTopGroupBox, 10)
        self.peopleMainLayout.addWidget(self.peopleMiddleGroupBox, 10)
        self.peopleMainLayout.addLayout(self.peopleMainBottomLayout, 80)

        self.setLayout(self.peopleMainLayout)

