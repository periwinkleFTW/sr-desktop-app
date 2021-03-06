from PySide2.QtCore import Qt, Slot
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
    QTableWidgetItem, QTableWidget, QGroupBox, QCheckBox, QAbstractItemView, QTableView, QMessageBox, \
    QFileDialog, QHeaderView, QSpacerItem, QSizePolicy
from PySide2.QtGui import QPixmap

import datetime
import csv
import xlsxwriter
import sys

from backend import Database
from add_issue import AddIssue
from display_issue import DisplayIssue
from generator_pdf import PDF
from generator_csv import CSV
import styles

db = Database("sr-data.db")


class IssuesTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.IssueTitle = 'ISSUES'

        self.UI()

    @property
    def Title(self):
        return self.IssueTitle

    def UI(self):
        self.widgets()
        self.layouts()
        self.funcDisplayIssues()

    def widgets(self):
        # Issues widgets ###########################################################
        # Top layout (search issues) widgets
        self.searchIssuesText = QLabel("Search: ")
        self.searchIssuesEntry = QLineEdit()
        self.searchIssuesEntry.setPlaceholderText("Search issues..")
        self.searchIssuesBtn = QPushButton("Search")
        self.searchIssuesBtn.setObjectName("btn_searchIssues")
        self.searchIssuesBtn.clicked.connect(self.funcSearchIssues)
        self.refreshIssuesBtn = QPushButton("Refresh")
        self.refreshIssuesBtn.clicked.connect(self.funcDisplayIssues)

        # Middle layout (list issues) widgets with radio buttons
        self.allIssuesRadioBtn = QRadioButton("All issues")
        self.ongoingIssuesRadioBtn = QRadioButton("Pending issues")
        self.lateIssuesRadioBtn = QRadioButton("Late issues")
        self.closedIssuesRadioBtn = QRadioButton("Closed issues")
        self.listIssuesBtn = QPushButton("List")
        self.listIssuesBtn.setObjectName("btn_listIssues")
        self.listIssuesBtn.clicked.connect(self.funcListIssues)

        # Bottom layout widget
        # Table showing issues
        self.issuesTable = QTableWidget()
        self.issuesTable.verticalHeader().hide()
        self.issuesTable.setSortingEnabled(True)
        self.issuesTable.setShowGrid(False)
        self.issuesTable.verticalHeader().setDefaultSectionSize(90)
        self.issuesTable.setColumnCount(13)

        self.issuesTable.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.issuesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.issuesTable.setHorizontalHeaderItem(1, QTableWidgetItem("Status"))
        self.issuesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.issuesTable.setHorizontalHeaderItem(2, QTableWidgetItem("ID"))
        self.issuesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Date"))
        self.issuesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Priority"))
        self.issuesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Observer"))
        self.issuesTable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.issuesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Inspection name"))
        self.issuesTable.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.issuesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Theme"))
        self.issuesTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.issuesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Facility"))
        self.issuesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Insp. Dept"))
        self.issuesTable.setHorizontalHeaderItem(10, QTableWidgetItem("Deadline"))
        self.issuesTable.setHorizontalHeaderItem(11, QTableWidgetItem("Status"))
        self.issuesTable.setHorizontalHeaderItem(12, QTableWidgetItem("Created on"))

        # Double clicking a row opens a window with issue details
        self.issuesTable.doubleClicked.connect(self.funcSelectedIssue)

        # Buttons for actions on selected issues
        self.addIssue = QPushButton("Add")
        self.addIssue.setObjectName("btn_addIssue")
        self.addIssue.clicked.connect(self.funcAddIssue)
        self.viewIssue = QPushButton("View/Edit")
        self.viewIssue.setObjectName("btn_viewIssue")
        self.viewIssue.clicked.connect(self.funcSelectedIssue)
        self.closeIssueBtn = QPushButton("Close")
        self.closeIssueBtn.setObjectName("btn_closeIssue")
        self.closeIssueBtn.clicked.connect(self.funcCloseIssue)
        self.deleteIssue = QPushButton("Delete")
        self.deleteIssue.setObjectName("btn_deleteIssue")
        self.deleteIssue.clicked.connect(self.funcDeleteIssue)

        self.exportIssuesCSVBtn = QPushButton("Export CSV")
        self.exportIssuesCSVBtn.setEnabled(False)
        self.exportIssuesCSVBtn.setObjectName("btn_exportIssuesCSV")
        self.exportIssuesCSVBtn.clicked.connect(self.funcIssuesToCSV)

        self.exportIssuesXLSXBtn = QPushButton("Export XLSX")
        self.exportIssuesXLSXBtn.setEnabled(False)
        self.exportIssuesXLSXBtn.setObjectName("btn_exportIssuesXLSX")
        self.exportIssuesXLSXBtn.clicked.connect(self.funcIssuestoXLSX)

        self.exportIssuesPDFBtn = QPushButton("Export PDF")
        self.exportIssuesPDFBtn.setEnabled(False)
        self.exportIssuesPDFBtn.setObjectName("btn_exportIssuesPDF")
        self.exportIssuesPDFBtn.clicked.connect(self.funcIssuesToPdf)

    def layouts(self):
        # Issues layouts ###########################################################
        self.issuesMainLayout = QVBoxLayout()
        self.issuesMainTopLayout = QHBoxLayout()
        self.issuesTopLeftLayout = QHBoxLayout()
        self.issuesTopRightLayout = QHBoxLayout()
        # self.issuesMainMiddleLayout = QHBoxLayout()
        self.issuesMainBottomLayout = QHBoxLayout()
        self.issuesBottomRightLayout = QVBoxLayout()
        self.issuesBottomLeftLayout = QHBoxLayout()
        # Groupboxes allow customization using CSS-like syntax
        # self.issuesTopGroupBox = QGroupBox()
        # self.issuesTopGroupBoxRightFiller = QGroupBox()
        # self.issuesTopGroupBoxRightFiller.setStyleSheet(styles.groupBoxFillerStyle())
        #
        # self.issuesMiddleGroupBox = QGroupBox()
        # self.issuesMiddleGroupBoxRightFiller = QGroupBox()
        # self.issuesMiddleGroupBoxRightFiller.setStyleSheet(styles.groupBoxFillerStyle())

        self.issuesTopLeftGroupBox = QGroupBox()
        self.issuesTopRightGroupBox = QGroupBox()
        self.issuesTopGroupBox = QGroupBox()

        self.issuesBottomGroupBox = QGroupBox()
        self.issuesBottomLeftGroupBox = QGroupBox()
        self.issuesBottomRightGroupBox = QGroupBox()
        self.issuesBottomRightGroupBox.setStyleSheet('QGroupBox {margin-top: 0px;}')
        self.issuesBottomRightGroupBoxFiller = QGroupBox()
        self.issuesBottomRightGroupBoxFiller.setStyleSheet(styles.groupBoxFillerStyle())

        # Add widgets
        # Top layout (search box) widgets
        self.issuesTopLeftLayout.addWidget(self.searchIssuesText, 10)
        self.issuesTopLeftLayout.addWidget(self.searchIssuesEntry, 30)
        self.issuesTopLeftLayout.addWidget(self.searchIssuesBtn, 10)
        self.issuesTopLeftLayout.addItem(QSpacerItem(70, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.issuesTopLeftLayout.addWidget(self.refreshIssuesBtn, 10)
        self.issuesTopLeftGroupBox.setLayout(self.issuesTopLeftLayout)

        # layout (list box) widgets
        self.issuesTopRightLayout.addWidget(self.allIssuesRadioBtn)
        self.issuesTopRightLayout.addWidget(self.ongoingIssuesRadioBtn)
        self.issuesTopRightLayout.addWidget(self.lateIssuesRadioBtn)
        self.issuesTopRightLayout.addWidget(self.closedIssuesRadioBtn)
        self.issuesTopRightLayout.addWidget(self.listIssuesBtn)
        self.issuesTopRightGroupBox.setLayout(self.issuesTopRightLayout)

        self.issuesMainTopLayout.addWidget(self.issuesTopLeftGroupBox, 60)
        self.issuesMainTopLayout.addWidget(self.issuesTopRightGroupBox, 40)

        # Bottom layout (table with facilities) widgets
        # Bottom left layout with table
        self.issuesBottomLeftLayout.addWidget(self.issuesTable)
        self.issuesBottomLeftGroupBox.setLayout(self.issuesBottomLeftLayout)

        # Bottom right layout with buttons
        self.issuesBottomRightLayout.addWidget(self.addIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.viewIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.closeIssueBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.deleteIssue, 5)
        self.issuesBottomRightLayout.addWidget(self.issuesBottomRightGroupBoxFiller, 65)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesCSVBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesXLSXBtn, 5)
        self.issuesBottomRightLayout.addWidget(self.exportIssuesPDFBtn, 5)
        self.issuesBottomRightGroupBox.setLayout(self.issuesBottomRightLayout)

        self.issuesMainBottomLayout.addWidget(self.issuesTable, 90)
        self.issuesMainBottomLayout.addWidget(self.issuesBottomRightGroupBox, 10)

        self.issuesMainLayout.addLayout(self.issuesMainTopLayout, 10)
        self.issuesMainLayout.addLayout(self.issuesMainBottomLayout, 90)

        self.setLayout(self.issuesMainLayout)

    # Populating the table
    @Slot()
    def funcDisplayIssues(self):
        for i in reversed(range(self.issuesTable.rowCount())):
            self.issuesTable.removeRow(i)

        issues = db.cur.execute("SELECT "
                                "issue_id, "
                                "issue_date, "
                                "issue_priority, "
                                "issue_observer,"
                                "issue_inspection, "
                                "issue_theme, "
                                "issue_facility, "
                                "issue_insp_dept,"
                                "issue_deadline, "
                                "status, "
                                "created_on "
                                "FROM issues")

        for row_data in issues:
            row_number = self.issuesTable.rowCount()
            self.issuesTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            checkbox.stateChanged.connect(self.funcActivateBtnsWithCheckbox)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignCenter)
            self.issuesTable.setCellWidget(row_number, 0, qwidget)
            self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))
            # Add status photos_thumbnails to the table
            thumbStatusWidget = QWidget()
            # Assign proper status thumbnails based on deadline
            if row_data[9] == "Closed":
                pic = QPixmap('assets/icons/issue_icons/issue_closed_icon.png')
            elif row_data[8] > str(datetime.datetime.now()):
                pic = QPixmap('assets/icons/issue_icons/issue_pending_icon.png')
            elif row_data[8] < str(datetime.datetime.now()):
                pic = QPixmap('assets/icons/issue_icons/issue_late_icon.png')

            thumbStatusLabel = QLabel()
            thumbStatusLabel.setPixmap(pic)
            thumbStatusLayout = QHBoxLayout(thumbStatusWidget)
            thumbStatusLayout.addWidget(thumbStatusLabel)
            self.issuesTable.setCellWidget(row_number, 1, thumbStatusWidget)
            self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))

            thumbPriorityWidget = QWidget()
            # Assign priority thumbnails
            if row_data[2] == "Low":
                pic = QPixmap('assets/icons/issue_priority_icons/low_priority.png')
            elif row_data[2] == "Medium":
                pic = QPixmap('assets/icons/issue_priority_icons/medium_priority.png')
            elif row_data[2] == "High":
                pic = QPixmap('assets/icons/issue_priority_icons/high_priority.png')

            thumbPriorityLabel = QLabel()
            thumbPriorityLabel.setAlignment(Qt.AlignCenter)
            thumbPriorityLabel.setPixmap(pic)
            thumbPriorityLayout = QHBoxLayout(thumbPriorityWidget)
            thumbPriorityLayout.addWidget(thumbPriorityLabel)
            self.issuesTable.setCellWidget(row_number, 4, thumbPriorityWidget)
            self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))

            for column_number, data in enumerate(row_data, start=2):
                if column_number == 2:
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem("ISS#" + str(data)))
                elif column_number == 4:
                    # Do not print priority in the table
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(""))
                else:
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.issuesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.issuesTable.setSelectionBehavior(QTableView.SelectRows)

    @Slot()
    def funcActivateBtnsWithCheckbox(self):
        indices = self.funcIssuesCheckBox()

        if self.sender().isChecked() or indices:
            self.exportIssuesCSVBtn.setEnabled(True)
            self.exportIssuesXLSXBtn.setEnabled(True)
            self.exportIssuesPDFBtn.setEnabled(True)
        else:
            self.exportIssuesCSVBtn.setEnabled(False)
            self.exportIssuesXLSXBtn.setEnabled(False)
            self.exportIssuesPDFBtn.setEnabled(False)

    @Slot()
    def funcAddIssue(self):
        self.newIssue = AddIssue(self)
        self.newIssue.setObjectName("add_issue_popup")
        self.newIssue.setStyleSheet(styles.addPopups())

    @Slot()
    def funcIssuesCheckBox(self):
        checked_list = []
        for i in range(self.issuesTable.rowCount()):
            if self.issuesTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.issuesTable.item(i, 2).text()
                checked_list.append(item.lstrip("ISS#"))
        return checked_list


    @Slot()
    def funcSelectedIssue(self):
        self.displayIssue = DisplayIssue(self)

    @Slot()
    def funcSearchIssues(self):
        value = self.searchIssuesEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.funcDisplayIssues()
        else:
            # Erase search entry
            self.searchIssuesEntry.setText("")
            try:
                query = "SELECT * FROM issues WHERE " \
                        "issue_id LIKE ? " \
                        "OR issue_date LIKE ?" \
                        "OR issue_priority LIKE ?" \
                        "OR issue_observer LIKE ?" \
                        "OR issue_team LIKE ?" \
                        "OR issue_inspection LIKE ?" \
                        "OR issue_theme LIKE ?" \
                        "OR issue_facility LIKE ?" \
                        "OR issue_fac_supervisor LIKE ?" \
                        "OR issue_spec_loc LIKE ?" \
                        "OR issue_insp_dept LIKE ?" \
                        "OR issue_insp_contr LIKE ?" \
                        "OR issue_insp_subcontr LIKE ?" \
                        "OR issue_deadline LIKE ?"
                results = db.cur.execute(query,
                                         ('%' + value + '%', '%' + value + '%',
                                          '%' + value + '%', '%' + value + '%',
                                          '%' + value + '%', '%' + value + '%',
                                          '%' + value + '%', '%' + value + '%',
                                          '%' + value + '%', '%' + value + '%',
                                          '%' + value + '%', '%' + value + '%',
                                          '%' + value + '%', '%' + value + '%',)).fetchall()
                if results == []:
                    QMessageBox.information(self, "Info", "Nothing was found")
                    self.funcDisplayIssues()
                else:
                    for i in reversed(range(self.issuesTable.rowCount())):
                        self.issuesTable.removeRow(i)

                    for row_data in results:
                        row_number = self.issuesTable.rowCount()
                        self.issuesTable.insertRow(row_number)
                        # Add checkboxes to the table
                        qwidget = QWidget()
                        checkbox = QCheckBox()
                        checkbox.setCheckState(Qt.Unchecked)
                        qhboxlayout = QHBoxLayout(qwidget)
                        qhboxlayout.addWidget(checkbox)
                        qhboxlayout.setAlignment(Qt.AlignCenter)
                        self.issuesTable.setCellWidget(row_number, 0, qwidget)
                        self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))
                        for column_number, data in enumerate(row_data, start=1):
                            if column_number == 1:
                                self.issuesTable.setItem(row_number, column_number,
                                                         QTableWidgetItem("ISS#" + str(data)))
                            else:
                                self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            except:
                QMessageBox.information(self, "Info", "Cannot access database")

    @Slot()
    def funcListIssues(self):
        try:
            if self.allIssuesRadioBtn.isChecked():
                self.funcDisplayIssues()
            elif self.ongoingIssuesRadioBtn.isChecked():
                query = "SELECT " \
                        "issue_id, " \
                        "issue_date, " \
                        "issue_priority, " \
                        "issue_observer," \
                        "issue_inspection, " \
                        "issue_theme, " \
                        "issue_facility, " \
                        "issue_insp_dept," \
                        "issue_deadline, " \
                        "status, " \
                        "created_on " \
                        "FROM issues WHERE status='Open' " \
                        "AND issue_deadline > DATETIME('now')"
                issues = db.cur.execute(query).fetchall()

                for i in reversed(range(self.issuesTable.rowCount())):
                    self.issuesTable.removeRow(i)

                for row_data in issues:
                    row_number = self.issuesTable.rowCount()
                    self.issuesTable.insertRow(row_number)
                    # Add checkboxes to the table
                    qwidget = QWidget()
                    checkbox = QCheckBox()
                    checkbox.setCheckState(Qt.Unchecked)
                    qhboxlayout = QHBoxLayout(qwidget)
                    qhboxlayout.addWidget(checkbox)
                    qhboxlayout.setAlignment(Qt.AlignCenter)
                    self.issuesTable.setCellWidget(row_number, 0, qwidget)
                    self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))
                    for column_number, data in enumerate(row_data, start=1):
                        if column_number == 1:
                            self.issuesTable.setItem(row_number, column_number,
                                                     QTableWidgetItem("ISS#" + str(data)))
                        else:
                            self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            elif self.lateIssuesRadioBtn.isChecked():
                query = "SELECT issue_id, " \
                        "issue_date, " \
                        "issue_priority, " \
                        "issue_observer," \
                        "issue_inspection, " \
                        "issue_theme, " \
                        "issue_facility, " \
                        "issue_insp_dept," \
                        "issue_deadline, " \
                        "status, " \
                        "created_on " \
                        "FROM issues " \
                        "WHERE status='Open' AND issue_deadline < DATETIME('now')"
                issues = db.cur.execute(query).fetchall()

                for i in reversed(range(self.issuesTable.rowCount())):
                    self.issuesTable.removeRow(i)

                for row_data in issues:
                    row_number = self.issuesTable.rowCount()
                    self.issuesTable.insertRow(row_number)
                    # Add checkboxes to the table
                    qwidget = QWidget()
                    checkbox = QCheckBox()
                    checkbox.setCheckState(Qt.Unchecked)
                    qhboxlayout = QHBoxLayout(qwidget)
                    qhboxlayout.addWidget(checkbox)
                    qhboxlayout.setAlignment(Qt.AlignCenter)
                    self.issuesTable.setCellWidget(row_number, 0, qwidget)
                    self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))
                    for column_number, data in enumerate(row_data, start=1):
                        if column_number == 1:
                            self.issuesTable.setItem(row_number, column_number,
                                                     QTableWidgetItem("ISS#" + str(data)))
                        else:
                            self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            elif self.closedIssuesRadioBtn.isChecked():
                query = "SELECT " \
                        "issue_id, " \
                        "issue_date, " \
                        "issue_priority, " \
                        "issue_observer," \
                        "issue_inspection, " \
                        "issue_theme, " \
                        "issue_facility, " \
                        "issue_insp_dept," \
                        "issue_deadline, " \
                        "status, " \
                        "created_on " \
                        "FROM issues WHERE status='Closed'"
                issues = db.cur.execute(query).fetchall()

                for i in reversed(range(self.issuesTable.rowCount())):
                    self.issuesTable.removeRow(i)

                for row_data in issues:
                    row_number = self.issuesTable.rowCount()
                    self.issuesTable.insertRow(row_number)
                    # Add checkboxes to the table
                    qwidget = QWidget()
                    checkbox = QCheckBox()
                    checkbox.setCheckState(Qt.Unchecked)
                    qhboxlayout = QHBoxLayout(qwidget)
                    qhboxlayout.addWidget(checkbox)
                    qhboxlayout.setAlignment(Qt.AlignCenter)
                    self.issuesTable.setCellWidget(row_number, 0, qwidget)
                    self.issuesTable.setItem(row_number, 0, QTableWidgetItem(row_number))
                    for column_number, data in enumerate(row_data, start=1):
                        if column_number == 1:
                            self.issuesTable.setItem(row_number, column_number,
                                                     QTableWidgetItem("ISS#" + str(data)))
                        else:
                            self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        except:
            QMessageBox.information(self, "Info", "Cannot access database")

    @Slot()
    def funcCloseIssue(self):
        indices = self.funcIssuesCheckBox()
        # Close issues with selected checkboxes
        if indices:
            try:
                for index in range(len(indices)):
                    statusQuery = "SELECT status FROM issues WHERE issue_id=?"
                    currentStatus = db.cur.execute(statusQuery, (indices[index],)).fetchone()

                    if currentStatus[0] == "Open":
                        query = "UPDATE issues SET status='Closed' WHERE issue_id=?"

                        db.cur.execute(query, (indices[index],))
                        db.conn.commit()
                    else:
                        QMessageBox.information(self, "Info", "Issue(s) is already closed")

                QMessageBox.information(self, "Info", "Operation completed successfully")
                self.funcDisplayIssues()

            except:
                QMessageBox.information(self, "Info", "Something went wrong")
        else:
            row = self.issuesTable.currentRow()
            issueId = self.issuesTable.item(row, 2).text()
            issueId = issueId.lstrip("ISS#")

            try:
                statusQuery = "SELECT status FROM issues WHERE issue_id=?"
                currentStatus = db.cur.execute(statusQuery, (issueId,)).fetchone()

                if currentStatus[0] == "Open":
                    query = "UPDATE issues SET status='Closed' WHERE issue_id=?"

                    db.cur.execute(query, (issueId,))
                    db.conn.commit()

                    QMessageBox.information(self, "Info", "Issue closed successfully")
                    self.funcDisplayIssues()
                else:
                    QMessageBox.information(self, "Info", "Issue is already closed")

            except:
                QMessageBox.information(self, "Info", "Something went wrong")

    @Slot()
    def funcDeleteIssue(self):
        indices = self.funcIssuesCheckBox()

        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete selected issue(s)?",
                                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if (mbox == QMessageBox.Yes):
            if indices:
                try:
                    for index in range(len(indices)):
                        query = "DELETE FROM issues WHERE issue_id = ?"

                        db.cur.execute(query, (indices[index],))
                        db.conn.commit()

                    QMessageBox.information(self, "Info", "Issues were deleted")
                    self.funcDisplayIssues()
                except:
                    QMessageBox.information(self, "Info", "No changes made")
            else:
                row = self.issuesTable.currentRow()
                issueId = self.issuesTable.item(row, 2).text()
                issueId = issueId.lstrip("ISS#")
                try:
                    query = "DELETE FROM issues WHERE issue_id = ?"

                    db.cur.execute(query, (issueId,))
                    db.conn.commit()

                    QMessageBox.information(self, "Info", "Issue was deleted")
                    self.funcDisplayIssues()
                except:
                    QMessageBox.information(self, "Info", "No changes made")

            self.displayIssue.close()

    @Slot()
    def funcIssuesToCSV(self):
        indices = self.funcIssuesCheckBox()

        if indices:
            CSV(self, "issues", indices)
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")


    @Slot()
    def funcIssuestoXLSX(self):
        indices = self.funcIssuesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/IssuesXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM issues")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("Issues")
                    worksheet.set_column('A:C', 12)
                    worksheet.set_row(0, 30)
                    merge_format = workbook.add_format({
                        'bold': 1,
                        'align': 'center',
                        'valign': 'vcenter'})
                    worksheet.merge_range('A1:B1', '', merge_format)
                    worksheet.insert_image('A1', './assets/logo/logo-full-main.png',
                                           {'x_scale': 0.4, 'y_scale': 0.4, 'x_offset': 15, 'y_offset': 10})

                    # Create header row
                    stop = 17
                    col = 0
                    for i, value in enumerate(db.cur.description[:stop]):
                        worksheet.write(1, col, value[0])
                        col += 1

                    # Write data to xlsx file
                    row_number = 2
                    for index in range(len(indices)):
                        query = "SELECT * FROM issues WHERE issue_id=?"
                        issue_record = db.cur.execute(query, (indices[index],)).fetchone()
                        for i, value in enumerate(issue_record[:stop]):
                            if issue_record[18]:
                                worksheet.set_row(row_number, 185)
                                worksheet.set_column(17, 17, 35)
                                worksheet.insert_image(
                                    row_number, 17, issue_record[18],
                                    {'x_scale': 0.3, 'y_scale': 0.3})
                            worksheet.write(row_number, i, value)
                        row_number += 1

                    workbook.close()

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")

    @Slot()
    def funcIssuesToPdf(self):
        indices = self.funcIssuesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp it was created on to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/IssuesPDF" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".pdf",
                    "PDF files (*.pdf)")

                if fileName:
                    pdf = PDF()
                    pdf.add_page()
                    pdf.set_font('Arial', 'B', 13)

                    for index in range(len(indices)):
                        query = "SELECT * FROM issues WHERE issue_id=?"
                        issue_record = db.cur.execute(query, (indices[index],)).fetchone()

                        # This string allows for text formatting in the pdf, easy to implement and test
                        stringIssue = "\nIssue id: " + str(issue_record[0]) + \
                                      "\nIssue date: " + str(issue_record[1]) + \
                                      "\nPriority: " + str(issue_record[2]) + \
                                      "\nObserver: " + str(issue_record[3]) + \
                                      "\nRevision team: " + str(issue_record[4]) + \
                                      "\nInspection name: " + str(issue_record[5]) + \
                                      "\nHSE theme: " + str(issue_record[6]) + \
                                      "\nFacility: " + str(issue_record[7]) + \
                                      "\nFacility supervisor: " + str(issue_record[8]) + \
                                      "\nSpecific location: " + str(issue_record[9]) + \
                                      "\nInspected department: " + str(issue_record[10]) + \
                                      "\nInspected contractor: " + str(issue_record[11]) + \
                                      "\nInspected subcontractor: " + str(issue_record[12]) + \
                                      "\nDeadline: " + str(issue_record[13]) + \
                                      "\nStatus: " + str(issue_record[14]) + \
                                      "\nCreated on: " + str(issue_record[15]) + \
                                      "\nClosed on: " + str(issue_record[16])

                        effectivePageWidth = pdf.w - 2 * pdf.l_margin

                        ybefore = pdf.get_y()
                        pdf.multi_cell(effectivePageWidth / 2, 10, stringIssue)

                        if issue_record[18]:
                            pdf.set_xy(effectivePageWidth / 2 + pdf.l_margin, ybefore)
                            pdf.image(issue_record[18], effectivePageWidth / 2 + 20, 40, w=70)
                        pdf.ln(0.5)

                        # Page break is achieved by adding a new page
                        # after all items except for the last one
                        if index != (len(indices) - 1):
                            pdf.add_page()

                    pdf.output(fileName, 'F')

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))

            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")
