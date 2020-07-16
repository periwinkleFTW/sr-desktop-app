try:
    from PySide2.QtCore import Qt
    from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
        QTableWidgetItem, QTableWidget, QGroupBox, QCheckBox, QAbstractItemView, QTableView, QMessageBox, QFileDialog
except:
    from PyQt.QtCore import Qt
    from PyQt.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
        QTableWidgetItem, QTableWidget, QGroupBox, QCheckBox, QAbstractItemView, QTableView, QMessageBox, QFileDialog

import datetime
import csv
import xlsxwriter
import sys

from backend import Database
from add_issue import AddIssue
from display_issue import DisplayIssue
import styles

db = Database("sr-data.db")


class IssuesTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.IssueTitle = 'Issues'

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
        self.searchIssuesText = QLabel("Search issues: ")
        self.searchIssuesEntry = QLineEdit()
        self.searchIssuesEntry.setPlaceholderText("Type here..")
        self.searchIssuesBtn = QPushButton("Search")
        self.searchIssuesBtn.clicked.connect(self.funcSearchIssues)

        # Middle layout (list issues) widgets with radio buttons
        self.allIssuesRadioBtn = QRadioButton("All issues")
        self.ongoingIssuesRadioBtn = QRadioButton("Pending issues")
        self.lateIssuesRadioBtn = QRadioButton("Late issues")
        self.closedIssuesRadioBtn = QRadioButton("Closed issues")
        self.listIssuesBtn = QPushButton("List issues")
        self.listIssuesBtn.clicked.connect(self.funcListIssues)

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
        self.issuesTable.doubleClicked.connect(self.funcSelectedIssue)

        # Buttons for actions on selected issues
        self.refreshIssuesBtn = QPushButton("Refresh")
        self.refreshIssuesBtn.clicked.connect(self.funcDisplayIssues)
        self.addIssue = QPushButton("Add issue")
        self.addIssue.clicked.connect(self.funcAddIssue)
        self.viewIssue = QPushButton("View/Edit issue")
        self.viewIssue.clicked.connect(self.funcSelectedIssue)
        self.closeIssueBtn = QPushButton("Close issue")
        self.closeIssueBtn.clicked.connect(self.funcCloseIssue)
        self.deleteIssue = QPushButton("Delete issue")
        self.deleteIssue.clicked.connect(self.funcDeleteIssue)
        self.exportIssuesCSVBtn = QPushButton("Export CSV")
        self.exportIssuesCSVBtn.clicked.connect(self.funcIssuesToCSV)
        self.exportIssuesXLSXBtn = QPushButton("Export XLSX")
        self.exportIssuesXLSXBtn.clicked.connect(self.funcIssuestoXLSX)

    def layouts(self):
        # Issues layouts ###########################################################
        self.issuesMainLayout = QVBoxLayout()
        self.issuesMainTopLayout = QHBoxLayout()
        self.issuesMainMiddleLayout = QHBoxLayout()
        self.issuesMainBottomLayout = QHBoxLayout()
        self.issuesBottomRightLayout = QVBoxLayout()
        self.issuesBottomLeftLayout = QHBoxLayout()
        # Groupboxes allow customization using CSS-like syntax
        self.issuesTopGroupBox = QGroupBox()
        self.issuesTopGroupBoxRightFiller = QGroupBox()
        self.issuesTopGroupBoxRightFiller.setStyleSheet(styles.groupBoxFillerStyle())

        self.issuesMiddleGroupBox = QGroupBox()
        self.issuesMiddleGroupBoxRightFiller = QGroupBox()
        self.issuesMiddleGroupBoxRightFiller.setStyleSheet(styles.groupBoxFillerStyle())


        self.issuesBottomGroupBox = QGroupBox()
        self.issuesBottomLeftGroupBox = QGroupBox()

        self.issuesBottomRightGroupBox = QGroupBox()
        self.issuesBottomRightGroupBoxFiller = QGroupBox()
        self.issuesBottomRightGroupBoxFiller.setStyleSheet(styles.groupBoxFillerStyle())

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
    def funcDisplayIssues(self):
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

    def funcAddIssue(self):
        self.newIssue = AddIssue(self)

    def funcIssuesCheckBox(self):
        checked_list = []
        for i in range(self.issuesTable.rowCount()):
            if self.issuesTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.issuesTable.item(i, 0).text()
                checked_list.append(item.lstrip("ISS#"))
        return checked_list

    def funcSelectedIssue(self):
        self.displayIssue = DisplayIssue(self)

    def funcSearchIssues(self):
        value = self.searchIssuesEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.funcDisplayIssues()
        else:
            # Erase search entry
            self.searchIssuesEntry.setText("")
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
            results = db.cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%', '%' + value + '%',
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
                    for column_number, data in enumerate(row_data):
                        self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def funcListIssues(self):
        if self.allIssuesRadioBtn.isChecked():
            self.funcDisplayIssues()
        elif self.ongoingIssuesRadioBtn.isChecked():
            query = "SELECT * FROM issues WHERE status='Open' " \
                    "AND issue_deadline > DATETIME('now')"
            issues = db.cur.execute(query).fetchall()

            for i in reversed(range(self.issuesTable.rowCount())):
                self.issuesTable.removeRow(i)

            for row_data in issues:
                row_number = self.issuesTable.rowCount()
                self.issuesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.lateIssuesRadioBtn.isChecked():
            query = "SELECT * FROM issues WHERE status='Open' AND issue_deadline < DATETIME('now')"
            issues = db.cur.execute(query).fetchall()

            for i in reversed(range(self.issuesTable.rowCount())):
                self.issuesTable.removeRow(i)

            for row_data in issues:
                row_number = self.issuesTable.rowCount()
                self.issuesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.closedIssuesRadioBtn.isChecked():
            query = "SELECT * FROM issues WHERE status='Closed'"
            issues = db.cur.execute(query).fetchall()

            for i in reversed(range(self.issuesTable.rowCount())):
                self.issuesTable.removeRow(i)

            for row_data in issues:
                row_number = self.issuesTable.rowCount()
                self.issuesTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.issuesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

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
            issueId = self.issuesTable.item(row, 0).text()
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
                issueId = self.issuesTable.item(row, 0).text()
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

    def funcIssuesToCSV(self):
        indices = self.funcIssuesCheckBox()
        # Check if there are any selected items
        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportIssCSV" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".csv",
                    "CSV files (*.csv)")
                if fileName:
                    with open(fileName, "w") as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter="|")
                        # Setting cursor on the correct table
                        db.cur.execute("SELECT * FROM issues")
                        # Get headers
                        csv_writer.writerow([i[0] for i in db.cur.description])
                        for index in indices:
                            query = "SELECT * FROM issues WHERE issue_id=?"
                            facility_record = db.cur.execute(query, (index,)).fetchone()
                            csv_writer.writerow(facility_record)

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")

    def funcIssuestoXLSX(self):
        indices = self.funcIssuesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/exportIssXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM issues")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("Issues")

                    # Create header row
                    col = 0
                    for value in db.cur.description:
                        worksheet.write(0, col, value[0])
                        col += 1

                    # Write date to xlsx file
                    row_number = 1
                    for index in range(len(indices)):
                        query = "SELECT * FROM issues WHERE issue_id=?"
                        issue_record = db.cur.execute(query, (indices[index],)).fetchone()
                        for i, value in enumerate(issue_record):
                            worksheet.write(row_number, i, value)
                        row_number += 1

                    workbook.close()

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")
