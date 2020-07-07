from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
    QTableWidgetItem, QTableWidget, QGroupBox, QCheckBox, QAbstractItemView, QTableView
from PySide2.QtCore import Qt

from backend import Database
from issues_actions import IssuesActions

db = Database("sr-data.db")


class IssuesTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)

        self.Parent = parent

        self.actions = IssuesActions(self)

        self.UI()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Issues widgets ###########################################################
        # Top layout (search issues) widgets
        self.searchIssuesText = QLabel("Search issues: ")
        self.searchIssuesEntry = QLineEdit()
        self.searchIssuesEntry.setPlaceholderText("Search issues..")
        self.searchIssuesBtn = QPushButton("Search")
        # self.searchIssuesBtn.clicked.connect(self.searchIssues)

        # Middle layout (list issues) widgets with radio buttons
        self.allIssuesRadioBtn = QRadioButton("All issues")
        self.ongoingIssuesRadioBtn = QRadioButton("Pending issues")
        self.lateIssuesRadioBtn = QRadioButton("Late issues")
        self.closedIssuesRadioBtn = QRadioButton("Closed issues")
        self.listIssuesBtn = QPushButton("List issues")
        # self.listIssuesBtn.clicked.connect(self.listIssues)

        # Bottom layout widget
        # Table showing issues
        self.issuesTable = QTableWidget()
        self.issuesTable.setColumnCount(16)
        # self.issuesTable.setColumnHidden(0, True)
        self.issuesTable.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
        self.issuesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Date"))
        self.issuesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Priority"))
        self.issuesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Observer"))
        self.issuesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Rev. Team"))
        self.issuesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Inspection name"))
        self.issuesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Theme"))
        self.issuesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Facility"))
        self.issuesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Facility Superv."))
        self.issuesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Spec. Loc."))
        self.issuesTable.setHorizontalHeaderItem(10, QTableWidgetItem("Insp. Dept"))
        self.issuesTable.setHorizontalHeaderItem(11, QTableWidgetItem("Insp. Contr."))
        self.issuesTable.setHorizontalHeaderItem(12, QTableWidgetItem("Subcontr"))
        self.issuesTable.setHorizontalHeaderItem(13, QTableWidgetItem("Deadline"))
        self.issuesTable.setHorizontalHeaderItem(14, QTableWidgetItem("Status"))
        self.issuesTable.setHorizontalHeaderItem(15, QTableWidgetItem("Created on"))

        # Double clicking a row opens a window with issue details
        # self.issuesTable.doubleClicked.connect(self.selectedIssue)

        # Buttons for actions on selected issues
        self.refreshIssuesBtn = QPushButton("Refresh")
        # self.refreshIssuesBtn.clicked.connect(self.displayIssues)
        self.addIssue = QPushButton("Add issue")
        self.addIssue.clicked.connect(self.actions.funcAddIssue)
        self.viewIssue = QPushButton("View/Edit issue")
        # self.viewIssue.clicked.connect(self.selectedIssue)
        self.closeIssueBtn = QPushButton("Close issue")
        # self.closeIssueBtn.clicked.connect(self.funcCloseIssue)
        self.deleteIssue = QPushButton("Delete issue")
        # self.deleteIssue.clicked.connect(self.funcDeleteIssue)
        self.exportIssuesCSVBtn = QPushButton("Export CSV")
        # self.exportIssuesCSVBtn.clicked.connect(self.funcIssuesToCSV)
        self.exportIssuesXLSXBtn = QPushButton("Export XLSX")
        # self.exportIssuesXLSXBtn.clicked.connect(self.funcIssuestoXLSX)

    def layouts(self):
        # Issues layouts ###########################################################
        self.issuesMainLayout = QVBoxLayout()
        self.issuesMainTopLayout = QHBoxLayout()
        self.issuesMainMiddleLayout = QHBoxLayout()
        self.issuesMainBottomLayout = QHBoxLayout()
        self.issuesBottomRightLayout = QVBoxLayout()
        self.issuesBottomLeftLayout = QHBoxLayout()
        # Groupboxes allow customization using CSS-like syntax
        self.issuesTopGroupBox = QGroupBox("Search Box")
        self.issuesTopGroupBoxRightFiller = QGroupBox()
        self.issuesMiddleGroupBox = QGroupBox("List Box")
        self.issuesMiddleGroupBoxRightFiller = QGroupBox()
        self.issuesBottomGroupBox = QGroupBox()
        self.issuesBottomLeftGroupBox = QGroupBox("Issues")
        self.issuesBottomRightGroupBox = QGroupBox("Actions")
        self.issuesBottomRightGroupBoxFiller = QGroupBox()

        # Add widgets
        # Top layout (search box) widgets
        self.issuesMainTopLayout.addWidget(self.searchIssuesText, 10)
        self.issuesMainTopLayout.addWidget(self.searchIssuesEntry, 30)
        self.issuesMainTopLayout.addWidget(self.searchIssuesBtn, 10)
        self.issuesMainTopLayout.addWidget(self.issuesTopGroupBoxRightFiller, 50)
        self.issuesTopGroupBox.setLayout(self.issuesMainTopLayout)

        # Middle layout (list box) widgets
        self.issuesMainMiddleLayout.addWidget(self.allIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.ongoingIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.lateIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.closedIssuesRadioBtn)
        self.issuesMainMiddleLayout.addWidget(self.listIssuesBtn)
        self.issuesMainMiddleLayout.addWidget(self.issuesMiddleGroupBoxRightFiller, 65)
        self.issuesMiddleGroupBox.setLayout(self.issuesMainMiddleLayout)

        # Bottom layout (table with facilities) widgets
        # Bottom left layout with table
        self.issuesBottomLeftLayout.addWidget(self.issuesTable)
        self.issuesBottomLeftGroupBox.setLayout(self.issuesBottomLeftLayout)

        # Bottom right layout with buttons
        self.issuesBottomRightLayout.addWidget(self.refreshIssuesBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.addIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.viewIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.closeIssueBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.deleteIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.issuesBottomRightGroupBoxFiller, 65)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesCSVBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesXLSXBtn, 5)
        self.issuesBottomRightGroupBox.setLayout(self.issuesBottomRightLayout)

        self.issuesMainBottomLayout.addWidget(self.issuesBottomLeftGroupBox, 90)
        self.issuesMainBottomLayout.addWidget(self.issuesBottomRightGroupBox, 10)

        self.issuesMainLayout.addWidget(self.issuesTopGroupBox, 10)
        self.issuesMainLayout.addWidget(self.issuesMiddleGroupBox, 10)
        self.issuesMainLayout.addLayout(self.issuesMainBottomLayout, 80)

        self.setLayout(self.issuesMainLayout)

    # Populating the table
    def displayIssues(self):
        for i in reversed(range(self.issuesTable.rowCount())):
            self.issuesTable.removeRow(i)

        issues = db.cur.execute("SELECT * FROM issues")

        for row_data in issues:
            row_number = self.issuesTable.rowCount()
            self.issuesTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignRight)
            qhboxlayout.setContentsMargins(0, 0, 20, 0)
            self.issuesTable.setCellWidget(row_number, 0, qwidget)
            self.issuesTable.setItem(row_number, 1, QTableWidgetItem(str(row_number)))

            for column_number, data in enumerate(row_data):
                if column_number == 0:
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem("ISS#" + str(data)))
                else:
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.issuesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.issuesTable.setSelectionBehavior(QTableView.SelectRows)
