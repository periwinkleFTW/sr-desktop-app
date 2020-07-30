
import os
import random
import string
from os import path as osPath
from shutil import copy2 as ShCopy2

from PySide2.QtCore import QDateTime
from PySide2.QtGui import QIcon, QPixmap, Qt
from PySide2.QtWidgets import QWidget, QScrollArea, QLabel, QDateTimeEdit, QComboBox, QTextEdit, \
    QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame, QMessageBox, QFileDialog
from backend import Database

db = Database("sr-data.db")

defaultImg = "assets/icons/logo-dark.png"


class AddIssue(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("Add issue")
        self.setWindowIcon(QIcon("assets/icons/icon.ico"))
        self.setGeometry(450, 150, 750, 950)
        # self.setFixedSize(self.size())

        self.Parent = parent

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)

        # Top layout widgets
        self.addIssueImg = QLabel()
        self.img = QPixmap('assets/icons/create-issue.png')
        self.addIssueImg.setPixmap(self.img)
        self.addIssueImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add issue")
        self.titleText.setObjectName("add_issue_title")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Middle layout widgets
        # self.issueInfoTitleText = QLabel("Issue info")
        # self.issueInfoTitleText.setAlignment(Qt.AlignCenter)
        self.dateEntry = QDateTimeEdit()
        self.dateEntry.setDateTime(QDateTime.currentDateTime())
        self.priorityEntry = QComboBox()
        self.priorityEntry.setEditable(True)
        self.observerEntry = QComboBox()
        self.observerEntry.setEditable(True)
        self.revisionTeamEntry = QComboBox()
        self.revisionTeamEntry.setEditable(True)
        self.inspectionNameEntry = QComboBox()
        self.inspectionNameEntry.setEditable(True)
        self.observationThemeEntry = QComboBox()
        self.observationThemeEntry.setEditable(True)
        self.facilityEntry = QComboBox()
        self.facilityEntry.setEditable(True)
        self.facilitySupervisorEntry = QComboBox()
        self.facilitySupervisorEntry.setEditable(True)
        self.specificLocationEntry = QTextEdit()
        self.inspectedDepartmentEntry = QComboBox()
        self.inspectedDepartmentEntry.setEditable(True)
        self.inspectedContractorEntry = QComboBox()
        self.inspectedContractorEntry.setEditable(True)
        self.inspectedSubcontractorEntry = QComboBox()
        self.inspectedSubcontractorEntry.setEditable(True)
        self.deadlineEntry = QDateTimeEdit()
        self.deadlineEntry.setDateTime(QDateTime.currentDateTime())

        # Bottom layout widgets
        self.attachFilesBtn = QPushButton("Attach files")
        self.attachFilesBtn.clicked.connect(self.funcAttachFiles)
        self.addActionBtn = QPushButton("Add action")

        self.rootCauseEntry = QComboBox()
        self.rootCauseEntry.setEditable(True)
        self.rootCauseDetailsEntry = QTextEdit()
        self.rootCauseActionPartyEntry = QComboBox()
        self.rootCauseActionPartyEntry.setEditable(True)
        self.addRootCauseBtn = QPushButton("Add root cause")

        self.submitObservationBtn = QPushButton("Add issue")
        self.submitObservationBtn.clicked.connect(self.addIssue)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.closeWindow)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()

        # Put elements into frames for visual distinction
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets to top layout
        # self.topLayout.addWidget(self.addIssueImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        # self.bottomLayout.addRow(self.issueInfoTitleText)
        self.bottomLayout.addRow(QLabel("Inspection Date: "), self.dateEntry)
        self.bottomLayout.addRow(QLabel("Priority: "), self.priorityEntry)
        self.bottomLayout.addRow(QLabel("Observer: "), self.observerEntry)
        self.bottomLayout.addRow(QLabel("Revision Team: "), self.revisionTeamEntry)
        self.bottomLayout.addRow(QLabel("Inspection Name: "), self.inspectionNameEntry)
        self.bottomLayout.addRow(QLabel("HSE Theme: "), self.observationThemeEntry)
        self.bottomLayout.addRow(QLabel("Facility: "), self.facilityEntry)
        self.bottomLayout.addRow(QLabel("Facility supervisor: "), self.facilitySupervisorEntry)
        self.bottomLayout.addRow(QLabel("Specific location: "), self.specificLocationEntry)
        self.bottomLayout.addRow(QLabel("Inspected department: "), self.inspectedDepartmentEntry)
        self.bottomLayout.addRow(QLabel("Inspected contractor: "), self.inspectedContractorEntry)
        self.bottomLayout.addRow(QLabel("Inspected subcontractor: "), self.inspectedSubcontractorEntry)
        self.bottomLayout.addRow(QLabel("Deadline: "), self.deadlineEntry)

        self.bottomLayout.addRow(QLabel(""), self.attachFilesBtn)
        # self.bottomLayout.addRow(QLabel(""), self.addActionBtn)

        # self.bottomLayout.addRow(QLabel(""), self.addRootCauseBtn)
        self.bottomLayout.addRow(QLabel(""), self.submitObservationBtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        # Make bottom frame scollable
        self.scroll.setWidget(self.bottomFrame)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.scroll)

        self.setLayout(self.mainLayout)

    def closeWindow(self):
        self.close()

    def addIssue(self):
        date = self.dateEntry.text()
        priority = self.priorityEntry.currentText()
        observer = self.observerEntry.currentText()
        revisionTeam = self.revisionTeamEntry.currentText()
        inspectionName = self.inspectionNameEntry.currentText()
        observationTheme = self.observationThemeEntry.currentText()
        facility = self.facilityEntry.currentText()
        facilitySupervisor = self.facilitySupervisorEntry.currentText()
        specificLocation = self.specificLocationEntry.toPlainText()
        inspectedDept = self.inspectedDepartmentEntry.currentText()
        inspectedContr = self.inspectedContractorEntry.currentText()
        inspectedSubcontr = self.inspectedSubcontractorEntry.currentText()
        deadline = self.deadlineEntry.text()

        if date and priority and observer and revisionTeam and inspectionName and observationTheme and facility\
                and facilitySupervisor and specificLocation and inspectedDept and inspectedContr \
                and inspectedSubcontr and deadline != "":
            try:
                query = "INSERT INTO issues (issue_date, issue_priority, issue_observer, issue_team," \
                        "issue_inspection, issue_theme, issue_facility, issue_fac_supervisor," \
                        "issue_spec_loc, issue_insp_dept, issue_insp_contr, issue_insp_subcontr, issue_deadline, created_on) " \
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                # The purpose of this block is to make created_on timestamp the same format as other dates
                currentTime = QDateTimeEdit()
                currentTime.setDateTime(QDateTime.currentDateTime())
                now = currentTime.text()

                db.cur.execute(query, (date, priority, observer, revisionTeam, inspectionName, observationTheme,
                                       facility, facilitySupervisor, specificLocation, inspectedDept, inspectedContr,
                                       inspectedSubcontr, deadline, now))
                db.conn.commit()

                QMessageBox.information(self, "Info", "Issue has been added")

                self.Parent.funcDisplayIssues()

                self.close()
            except:
                QMessageBox.information(self, "Info", "Issue has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")



    # Need to figure out how attach files to items in db
    def funcAttachFiles(self):
        # Check if the default directory for media exists, if not create one

        # if not os.path.isdir("./assets/media/issues-media"):
        #     os.makedirs("./assets/media/issues-media")
        # else:
        #     QMessageBox.information(self, "Info", "Cannot create media directory!")


        filePathName = QFileDialog.getOpenFileName(self, "Attach file...", "/", "Image files (*.jpg, *.jpeg, *.png)")[0]

        if osPath.isfile(filePathName):
            fileName, fileExt = osPath.splitext(filePathName)

            if fileExt == '.jpg' or fileExt == '.jpeg' or fileExt == '.png':
                randomSuffix = "".join(random.choice(string.ascii_lowercase) for i in range(6))
                newFilePath = ShCopy2(fileName+fileExt, "./assets/media/issues-media/"+randomSuffix+fileExt)

                return newFilePath

            else:
                QMessageBox.information(self, "Info", "Wrong file type!")
        else:
            QMessageBox.information(self, "Info", "Something went wrong. Try again...")
