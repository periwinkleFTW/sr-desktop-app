from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QFrame, \
    QFormLayout, QMessageBox, QDateTimeEdit, QHBoxLayout, QSpacerItem, QSizePolicy, QTextEdit
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, QDateTime, Slot

import backend

from dropdown_menu_data import IssuesDropdownData

import styles

db = backend.Database("sr-data.db")


class DisplayIssue(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("View issue")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(450, 150, 750, 950)

        self.Parent = parent

        self.setStyleSheet(styles.mainStyle())

        self.UI()
        self.show()

    def UI(self):
        self.issueDetails()
        self.widgets()
        self.layouts()

    def issueDetails(self):
        row = self.Parent.issuesTable.currentRow()
        issueId = self.Parent.issuesTable.item(row, 2).text()
        # Strip the ISS# from the id
        issueId = issueId.lstrip("ISS#")

        query = "SELECT * FROM issues WHERE issue_id=?"

        cur = db.cur
        issue = cur.execute(query, (issueId,)).fetchone()

        self.id = issue[0]
        self.date = issue[1]
        self.priority = issue[2]
        self.observer = issue[3]
        self.revTeam = issue[4]
        self.inspectorName = issue[5]
        self.theme = issue[6]
        self.facility = issue[7]
        self.facilitySupervisor = issue[8]
        self.specLocation = issue[9]
        self.inspectedDept = issue[10]
        self.inspectedContr = issue[11]
        self.inspectedSubcontr = issue[12]
        self.deadline = issue[13]
        self.status = issue[14]

    def widgets(self):
        self.dropdownData = IssuesDropdownData()

        # Top layout widgets
        self.issueImg = QLabel()
        self.img = QPixmap('assets/icons/logo-dark.png')
        self.issueImg.setPixmap(self.img)
        self.issueImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display issue")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.idEntry = QLabel(str(self.id))

        self.dateEntry = QDateTimeEdit(calendarPopup=True)
        self.dateEntry.setDateTime(QDateTime.fromString(self.date, "yyyy-MM-dd h:mm AP"))

        self.priorityEntry = QComboBox()
        self.priorityEntry.addItems(self.dropdownData.priorityItems())
        self.priorityEntry.setCurrentText(self.priority)
        self.observerEntry = QComboBox()
        self.observerEntry.addItems(self.dropdownData.observerItems())
        self.observerEntry.setCurrentText(self.observer)
        self.revTeamEntry = QComboBox()
        self.revTeamEntry.addItems(self.dropdownData.revTeamItems())
        self.revTeamEntry.setCurrentText(self.revTeam)
        self.inspectionNameEntry = QComboBox()
        self.inspectionNameEntry.addItems(self.dropdownData.inspNameItems())
        self.inspectionNameEntry.setCurrentText(self.inspectorName)
        self.themeEntry = QComboBox()
        self.themeEntry.addItems(self.dropdownData.hseThemeItems())
        self.themeEntry.setCurrentText(self.theme)
        self.facilityEntry = QComboBox()
        self.facilityEntry.addItems(self.dropdownData.facilityItems())
        self.facilityEntry.setCurrentText(self.facility)
        self.facilitySupervisorEntry = QComboBox()
        self.facilitySupervisorEntry.addItems(self.dropdownData.facSupervisorItems())
        self.facilitySupervisorEntry.setCurrentText(self.facilitySupervisor)
        self.specLocationEntry = QTextEdit()
        self.specLocationEntry.setText(self.specLocation)
        self.inspectedDeptEntry = QComboBox()
        self.inspectedDeptEntry.addItems(self.dropdownData.inspDeptItems())
        self.inspectedDeptEntry.setCurrentText(self.inspectedDept)
        self.inspectedContrEntry = QComboBox()
        self.inspectedContrEntry.addItems(self.dropdownData.inspContrItems())
        self.inspectedContrEntry.setCurrentText(self.inspectedContr)
        self.inspectedSubcontrEntry = QComboBox()
        self.inspectedSubcontrEntry.addItems(self.dropdownData.inspSubcontrItems())
        self.inspectedSubcontrEntry.setCurrentText(self.inspectedSubcontr)
        self.statusEntry = QComboBox()
        self.statusEntry.addItems(self.dropdownData.statusItems())
        self.statusEntry.setCurrentText(self.status)
        self.deadlineEntry = QDateTimeEdit(calendarPopup=True)
        self.deadlineEntry.setDateTime(QDateTime.fromString(self.deadline, "yyyy-MM-dd h:mm AP"))

        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateIssue)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.Parent.funcDeleteIssue)
        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.closeWindow)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.bottomBtnLayout = QHBoxLayout()

        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.issueImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow("ID: ", self.idEntry)
        self.bottomLayout.addRow("Date: ", self.dateEntry)
        self.bottomLayout.addRow("Priority: ", self.priorityEntry)
        self.bottomLayout.addRow("Observer: ", self.observerEntry)
        self.bottomLayout.addRow("Revision Team: ", self.revTeamEntry)
        self.bottomLayout.addRow("Inspector name: ", self.inspectionNameEntry)
        self.bottomLayout.addRow("HSE theme: ", self.themeEntry)
        self.bottomLayout.addRow("Facility: ", self.facilityEntry)
        self.bottomLayout.addRow("Facility supervisor: ", self.facilitySupervisorEntry)
        self.bottomLayout.addRow("Specific location: ", self.specLocationEntry)
        self.bottomLayout.addRow("Inspected department: ", self.inspectedDeptEntry)
        self.bottomLayout.addRow("Inspected contractor: ", self.inspectedContrEntry)
        self.bottomLayout.addRow("Inspected subcontractor: ", self.inspectedSubcontrEntry)
        self.bottomLayout.addRow("Deadline: ", self.deadlineEntry)
        self.bottomLayout.addRow("Status: ", self.statusEntry)

        self.bottomBtnLayout.addWidget(self.cancelBtn)
        self.bottomBtnLayout.addItem(QSpacerItem(60, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.bottomBtnLayout.addWidget(self.deleteBtn)
        self.bottomBtnLayout.addWidget(self.updateBtn)

        self.bottomLayout.addRow(self.bottomBtnLayout)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    @Slot()
    def closeWindow(self):
        self.close()

    @Slot()
    def updateIssue(self):
        row = self.Parent.issuesTable.currentRow()
        issueId = self.Parent.issuesTable.item(row, 2).text()
        issueId = issueId.lstrip("ISS#")

        date = self.dateEntry.text()
        priority = self.priorityEntry.currentText()
        observer = self.observerEntry.currentText()
        revTeam = self.revTeamEntry.currentText()
        inspectionName = self.inspectionNameEntry.currentText()
        theme = self.themeEntry.currentText()
        facility = self.facilityEntry.currentText()
        facilitySupervisor = self.facilitySupervisorEntry.currentText()
        specLocation = self.specLocationEntry.toPlainText()
        inspDept = self.inspectedDeptEntry.currentText()
        inspContr = self.inspectedContrEntry.currentText()
        inspSubcontr = self.inspectedSubcontrEntry.currentText()
        status = self.statusEntry.currentText()
        print(status)
        deadline = self.deadlineEntry.text()

        if (date and priority and observer and revTeam and inspectionName and theme and facility
                and facilitySupervisor and specLocation and inspDept and deadline != ""):
            try:
                query = "UPDATE issues SET " \
                        "issue_date=?, " \
                        "issue_priority=?, " \
                        "issue_observer=?, " \
                        "issue_team=?," \
                        "issue_inspection=?, " \
                        "issue_theme=?, " \
                        "issue_facility=?, " \
                        "issue_fac_supervisor=?," \
                        "issue_spec_loc=?, " \
                        "issue_insp_dept=?, " \
                        "issue_insp_contr=?, " \
                        "issue_insp_subcontr=?," \
                        "issue_deadline=?, " \
                        "status=? " \
                        "WHERE issue_id=? "

                db.cur.execute(query, (date, priority, observer, revTeam, inspectionName, theme, facility,
                                       facilitySupervisor, specLocation, inspDept, inspContr, inspSubcontr,
                                       deadline, status, issueId))
                db.conn.commit()

                QMessageBox.information(self, "Info", "Issue info updated")
            except:
                QMessageBox.information(self, "Info", "No changes made")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")

        self.Parent.funcDisplayIssues()
        self.close()