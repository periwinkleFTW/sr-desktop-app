from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox, QFrame, \
    QFormLayout, QMessageBox
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt

import backend

db = backend.Database("sr-data.db")


class DisplayIssue(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("View issue")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(450, 150, 750, 650)

        self.Parent = parent

        self.UI()
        self.show()

    def UI(self):
        self.issueDetails()
        self.widgets()
        self.layouts()

    def issueDetails(self):
        row = self.Parent.issuesTable.currentRow()
        issueId = self.Parent.issuesTable.item(row, 0).text()
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
        # Top layout widgets
        self.issueImg = QLabel()
        self.img = QPixmap('assets/icons/logo-dark.png')
        self.issueImg.setPixmap(self.img)
        self.issueImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display issue")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.idEntry = QLabel(str(self.id))
        self.dateEntry = QLineEdit()
        self.dateEntry.setText(self.date)
        self.priorityEntry = QLineEdit()
        self.priorityEntry.setText(self.priority)
        self.observerEntry = QLineEdit()
        self.observerEntry.setText(self.observer)
        self.revTeamEntry = QLineEdit()
        self.revTeamEntry.setText(self.revTeam)
        self.inspectionNameEntry = QLineEdit()
        self.inspectionNameEntry.setText(self.inspectorName)
        self.themeEntry = QLineEdit()
        self.themeEntry.setText(self.theme)
        self.facilityEntry = QLineEdit()
        self.facilityEntry.setText(self.facility)
        self.facilitySupervisorEntry = QLineEdit()
        self.facilitySupervisorEntry.setText(self.facilitySupervisor)
        self.specLocationEntry = QLineEdit()
        self.specLocationEntry.setText(self.specLocation)
        self.inspectedDeptEntry = QLineEdit()
        self.inspectedDeptEntry.setText(self.inspectedDept)
        self.inspectedContrEntry = QLineEdit()
        self.inspectedContrEntry.setText(self.inspectedContr)
        self.inspectedSubcontrEntry = QLineEdit()
        self.inspectedSubcontrEntry.setText(self.inspectedSubcontr)
        self.statusEntry = QComboBox()
        self.statusEntry.setCurrentText(self.status)
        self.deadlineEntry = QLineEdit()
        self.deadlineEntry.setText(self.deadline)

        statusList = ["Open", "Closed"]
        self.statusEntry = QComboBox()
        self.statusEntry.addItems(statusList)

        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updateIssue)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.Parent.funcDeleteIssue)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
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
        self.bottomLayout.addRow("", self.updateBtn)
        self.bottomLayout.addRow("", self.deleteBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def updateIssue(self):
        row = self.Parent.issuesTable.currentRow()
        issueId = self.Parent.issuesTable.item(row, 0).text()
        issueId = issueId.lstrip("ISS#")

        date = self.dateEntry.text()
        priority = self.priorityEntry.text()
        observer = self.observerEntry.text()
        revTeam = self.revTeamEntry.text()
        inspectionName = self.inspectionNameEntry.text()
        theme = self.themeEntry.text()
        facility = self.facilityEntry.text()
        facilitySupervisor = self.facilitySupervisorEntry.text()
        specLocation = self.specLocationEntry.text()
        inspDept = self.inspectedDeptEntry.text()
        inspContr = self.inspectedContrEntry.text()
        inspSubcontr = self.inspectedSubcontrEntry.text()
        status_ = self.statusEntry.currentText()
        deadline = self.deadlineEntry.text()

        if (date and priority and observer and revTeam and inspectionName and theme and facility
                and facilitySupervisor and specLocation and inspDept and deadline != ""):
            try:
                query = "UPDATE issues SET issue_date=?, issue_priority=?, issue_observer=?, issue_team=?," \
                        "issue_inspection=?, issue_theme=?, issue_facility=?, issue_fac_supervisor=?," \
                        "issue_spec_loc=?, issue_insp_dept=?, issue_insp_contr=?, issue_insp_subcontr=?," \
                        "issue_deadline=?, status=? WHERE issue_id=? "

                db.cur.execute(query, (date, priority, observer, revTeam, inspectionName, theme, facility,
                                       facilitySupervisor, specLocation, inspDept, inspContr, inspSubcontr,
                                       deadline, status_, issueId))
                db.conn.commit()

                QMessageBox.information(self, "Info", "Issue info updated")
            except:
                QMessageBox.information(self, "Info", "No changes made")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")

        self.Parent.funcDisplayIssues()
        self.close()