
try:
    from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
        QTableWidgetItem, QTableWidget, QGroupBox, QHeaderView, QAbstractItemView, QTableView, QCheckBox, \
        QMessageBox, QFileDialog
    from PySide2.QtCore import Qt, Slot
except:
    from PyQt.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QRadioButton, QHBoxLayout, QVBoxLayout, \
        QTableWidgetItem, QTableWidget, QGroupBox, QHeaderView, QAbstractItemView, QTableView, QCheckBox, \
        QMessageBox, QFileDialog
    from PyQt.QtCore import Qt

import csv
import datetime
import xlsxwriter
import styles


from backend import Database
from add_person import AddPerson
from display_person import DisplayPerson
from pdf_generator import PDF

db = Database("sr-data.db")

class PeopleTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.PeoplTitle = 'PEOPLE'

        self.UI()

    @property
    def Title(self):
        return self.PeoplTitle

    def UI(self):
        self.widgets()
        self.layouts()
        self.funcDisplayPeople()

    def widgets(self):
        # People widgets ###########################################################
        # Top layout (search people) widgets
        self.searchPeopleText = QLabel("Search people: ")
        self.searchPeopleEntry = QLineEdit()
        self.searchPeopleEntry.setPlaceholderText("Search people..")
        self.searchPeopleBtn = QPushButton("Search")
        self.searchPeopleBtn.clicked.connect(self.searchPeople)

        # Middle layout (list people) widgets with radio buttons
        self.allPeopleRadioBtn = QRadioButton("All people")
        self.employeesPeopleRadioBtn = QRadioButton("Employees")
        self.contractorsPeopleRadioBtn = QRadioButton("Contractors")
        self.subcontractorsPeopleRadioBtn = QRadioButton("Subcontractors")
        self.listPeopleBtn = QPushButton("List people")
        self.listPeopleBtn.clicked.connect(self.funcListPeople)

        # Bottom layout widget, a table showing people
        self.peopleTable = QTableWidget()
        self.peopleTable.verticalHeader().hide()
        self.peopleTable.setSortingEnabled(True)
        self.peopleTable.setShowGrid(False)
        self.peopleTable.verticalHeader().setDefaultSectionSize(40)
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
        self.peopleTable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)

        # Double clicking a row opens a window with person details
        self.peopleTable.doubleClicked.connect(self.selectedPerson)

        # Buttons for actions on selected people
        self.addPerson = QPushButton("Add person")
        self.addPerson.clicked.connect(self.funcAddPerson)
        self.viewPerson = QPushButton("View/Edit person")
        self.viewPerson.clicked.connect(self.selectedPerson)
        self.deletePerson = QPushButton("Delete person")
        self.deletePerson.clicked.connect(self.funcDeletePerson)
        self.exportPeopleCSVBtn = QPushButton("Export CSV")
        self.exportPeopleCSVBtn.clicked.connect(self.funcPeopleToCSV)
        self.exportPeopleXLSXBtn = QPushButton("Export XLSX")
        self.exportPeopleXLSXBtn.clicked.connect(self.funcPeopleToXLSX)
        self.exportPeoplePDFBtn = QPushButton("Export PDF")
        self.exportPeoplePDFBtn.clicked.connect(self.funcPeopleToPdf)


    def layouts(self):
        # People layouts ###########################################################
        self.peopleMainLayout = QVBoxLayout()
        self.peopleMainTopLayout = QHBoxLayout()
        self.peopleTopLeftLayout = QHBoxLayout()
        self.peopleTopRightLayout = QHBoxLayout()

        # self.peopleMainMiddleLayout = QHBoxLayout()
        self.peopleMainBottomLayout = QHBoxLayout()
        self.peopleBottomRightLayout = QVBoxLayout()
        self.peopleBottomLeftLayout = QHBoxLayout()
        
        # Groupboxes allows customization using CSS-like syntax
        # self.peopleTopGroupBox = QGroupBox()
        # self.peopleTopGroupBoxRightFiller = QGroupBox()
        # self.peopleMiddleGroupBox = QGroupBox()
        # self.peopleMiddleGroupBoxRightFiller = QGroupBox()

        self.peopleTopLeftGroupBox = QGroupBox()
        self.peopleTopRightGroupBox = QGroupBox()
        self.peopleTopGroupBox = QGroupBox()

        self.peopleBottomGroupBox = QGroupBox()
        self.peopleBottomLeftGroupBox = QGroupBox()

        self.peopleBottomRightGroupBox = QGroupBox()
        self.peopleBottomRightGroupBox.setStyleSheet('QGroupBox {margin-top: 0px;}')
        self.peopleBottomRightGroupBoxFiller = QGroupBox()
        self.peopleBottomRightGroupBoxFiller.setStyleSheet(styles.groupBoxFillerStyle())

        # Top layout (search box) widgets
        self.peopleTopLeftLayout.addWidget(self.searchPeopleText, 10)
        self.peopleTopLeftLayout.addWidget(self.searchPeopleEntry, 30)
        self.peopleTopLeftLayout.addWidget(self.searchPeopleBtn, 10)
        self.peopleTopLeftGroupBox.setLayout(self.peopleTopLeftLayout)

        # Middle layout (list box) widgets
        self.peopleTopRightLayout.addWidget(self.allPeopleRadioBtn)
        self.peopleTopRightLayout.addWidget(self.employeesPeopleRadioBtn)
        self.peopleTopRightLayout.addWidget(self.contractorsPeopleRadioBtn)
        self.peopleTopRightLayout.addWidget(self.subcontractorsPeopleRadioBtn)
        self.peopleTopRightLayout.addWidget(self.listPeopleBtn)
        self.peopleTopRightGroupBox.setLayout(self.peopleTopRightLayout)

        self.peopleMainTopLayout.addWidget(self.peopleTopLeftGroupBox)
        self.peopleMainTopLayout.addWidget(self.peopleTopRightGroupBox)

        # Bottom layout (table with issues) widgets
        # Bottom left layout with table
        self.peopleBottomLeftLayout.addWidget(self.peopleTable)
        self.peopleBottomLeftGroupBox.setLayout(self.peopleBottomLeftLayout)

        # Bottom right layout with buttons
        self.peopleBottomRightLayout.addWidget(self.addPerson, 5)
        self.peopleBottomRightLayout.addWidget(self.viewPerson, 5)
        self.peopleBottomRightLayout.addWidget(self.deletePerson, 5)
        self.peopleBottomRightLayout.addWidget(self.peopleBottomRightGroupBoxFiller, 70)
        self.peopleBottomRightLayout.addWidget(self.exportPeopleCSVBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.exportPeopleXLSXBtn, 5)
        self.peopleBottomRightLayout.addWidget(self.exportPeoplePDFBtn, 5)
        self.peopleBottomRightGroupBox.setLayout(self.peopleBottomRightLayout)

        self.peopleMainBottomLayout.addWidget(self.peopleTable, 90)
        self.peopleMainBottomLayout.addWidget(self.peopleBottomRightGroupBox, 10)

        # self.peopleMainLayout.addWidget(self.peopleTopGroupBox, 10)
        # self.peopleMainLayout.addWidget(self.peopleMiddleGroupBox, 10)
        # self.peopleMainLayout.addLayout(self.peopleMainBottomLayout, 80)

        self.peopleMainLayout.addLayout(self.peopleMainTopLayout, 10)
        self.peopleMainLayout.addLayout(self.peopleMainBottomLayout, 90)

        self.setLayout(self.peopleMainLayout)

    @Slot()
    def funcDisplayPeople(self):
        for i in reversed(range(self.peopleTable.rowCount())):
            self.peopleTable.removeRow(i)

        cur = db.cur
        people = cur.execute("SELECT * FROM people")

        for row_data in people:
            row_number = self.peopleTable.rowCount()
            self.peopleTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignRight)
            qhboxlayout.setContentsMargins(0, 0, 20, 0)
            self.peopleTable.setCellWidget(row_number, 0, qwidget)
            self.peopleTable.setItem(row_number, 1, QTableWidgetItem(str(row_number)))

            for column_number, data in enumerate(row_data):
                if column_number == 0:
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem("PRN#" + str(data)))
                else:
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.peopleTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.peopleTable.setSelectionBehavior(QTableView.SelectRows)

    @Slot()
    def funcAddPerson(self):
        self.newPerson = AddPerson(self)
        self.newPerson.setObjectName("add_person_popup")
        self.newPerson.setStyleSheet(styles.addPopups())

    @Slot()
    def funcPeopleCheckBox(self):
        checked_list = []
        for i in range(self.peopleTable.rowCount()):
            if self.peopleTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.peopleTable.item(i, 0).text()
                checked_list.append(item.lstrip("PRN#"))
        return checked_list

    @Slot()
    def selectedPerson(self):
        self.displayPerson = DisplayPerson(self)
        self.displayPerson.show()

    @Slot()
    def funcDeletePerson(self):
        indices = self.funcPeopleCheckBox()

        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this person?",
                                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if (mbox == QMessageBox.Yes):
            if indices:
                try:
                    for index in range(len(indices)):
                        query = "DELETE FROM people WHERE person_id = ?"

                        db.cur.execute(query, (indices[index],))
                        db.conn.commit()

                    QMessageBox.information(self, "Info", "Selected people were deleted")
                    self.funcDisplayPeople()
                except:
                    QMessageBox.information(self, "Info", "No changes made")
            else:
                row = self.peopleTable.currentRow()
                personId = self.peopleTable.item(row, 0).text()
                personId = personId.lstrip("PRN#")
                try:
                    query = "DELETE FROM people WHERE person_id = ?"

                    db.cur.execute(query, (personId,))
                    db.conn.commit()

                    QMessageBox.information(self, "Info", "Person was deleted")
                    self.funcDisplayPeople()
                except:
                    QMessageBox.information(self, "Info", "No changes made")

        self.displayPerson.close()

    @Slot()
    def funcListPeople(self):
        if self.allPeopleRadioBtn.isChecked():
            self.funcDisplayPeople()
        elif self.employeesPeopleRadioBtn.isChecked():
            query = "SELECT * FROM people WHERE person_empl_type = 'Employee'"
            people = db.cur.execute(query).fetchall()

            for i in reversed(range(self.peopleTable.rowCount())):
                self.peopleTable.removeRow(i)

            for row_data in people:
                row_number = self.peopleTable.rowCount()
                self.peopleTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.contractorsPeopleRadioBtn.isChecked():
            query = "SELECT * FROM people WHERE person_empl_type = 'Contractor'"
            people = db.cur.execute(query).fetchall()

            for i in reversed(range(self.peopleTable.rowCount())):
                self.peopleTable.removeRow(i)

            for row_data in people:
                row_number = self.peopleTable.rowCount()
                self.peopleTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        elif self.subcontractorsPeopleRadioBtn.isChecked():
            query = "SELECT * FROM people WHERE person_empl_type = 'Subcontractor'"
            people = db.cur.execute(query).fetchall()

            for i in reversed(range(self.peopleTable.rowCount())):
                self.peopleTable.removeRow(i)

            for row_data in people:
                row_number = self.peopleTable.rowCount()
                self.peopleTable.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    @Slot()
    def searchPeople(self):
        value = self.searchPeopleEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.funcDisplayPeople()
        else:
            # Erase search entry
            self.searchPeopleEntry.setText("")
            query = "SELECT * FROM people WHERE " \
                    "person_id LIKE ? " \
                    "OR person_first_name LIKE ?" \
                    "OR person_last_name LIKE ?" \
                    "OR person_title LIKE ?" \
                    "OR person_phone LIKE ?" \
                    "OR person_email LIKE ?" \
                    "OR person_location LIKE ?" \
                    "OR person_empl_type LIKE ?"
            results = db.cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%', '%' + value + '%',
                                             '%' + value + '%', '%' + value + '%',)).fetchall()
            if results == []:
                QMessageBox.information(self, "Info", "Nothing was found")
                self.displayPeople()
            else:
                for i in reversed(range(self.peopleTable.rowCount())):
                    self.peopleTable.removeRow(i)

                for row_data in results:
                    row_number = self.peopleTable.rowCount()
                    self.peopleTable.insertRow(row_number)
                    for column_number, data in enumerate(row_data):
                        self.peopleTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    @Slot()
    def funcPeopleToCSV(self):
        indices = self.funcPeopleCheckBox()
        # Check if there are any selected items
        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/PeopleCSV" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".csv",
                    "CSV files (*.csv)")
                if fileName:
                    with open(fileName, "w") as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter="|")
                        # The purpose of this statement is to set cursor to correct table, needs rework because inefficient
                        db.cur.execute("SELECT * FROM people")
                        # Get headers from the table
                        csv_writer.writerow([i[0] for i in db.cur.description])
                        for index in indices:
                            query = "SELECT * FROM people WHERE person_id=?"
                            person_record = db.cur.execute(query, (index,)).fetchone()
                            csv_writer.writerow(person_record)

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select people to export")

    @Slot()
    def funcPeopleToXLSX(self):
        indices = self.funcPeopleCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/PeopleXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM people")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("People")

                    # Create header row
                    col = 0
                    for value in db.cur.description:
                        worksheet.write(0, col, value[0])
                        col += 1

                    # Write date to xlsx file
                    row_number = 1
                    for index in range(len(indices)):
                        query = "SELECT * FROM people WHERE person_id=?"
                        person_record = db.cur.execute(query, (indices[index],)).fetchone()
                        for i, value in enumerate(person_record):
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
    def funcPeopleToPdf(self):
        indices = self.funcPeopleCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/PeoplePDF" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".pdf",
                    "PDF files (*.pdf)")

                if fileName:
                    pdf = PDF()
                    pdf.add_page()
                    pdf.set_font('Arial', 'B', 13)

                    for index in range(len(indices)):
                        query = "SELECT * FROM people WHERE person_id=?"
                        person_record = db.cur.execute(query, (indices[index],)).fetchone()

                        # This string allows for text formatting in the pdf, easy to implement and test
                        stringPerson = "\nPerson id: " + str(person_record[0]) + "\nFirst name: " + str(person_record[1]) + \
                                      "\nLast name: " + str(person_record[2]) + "\nTitle: " + str(
                            person_record[3]) + \
                                      "\nPhone: " + str(person_record[4]) + "\nEmail: " + str(
                            person_record[5]) + \
                                      "\nLocation: " + str(person_record[6]) + "\nEmployment type: " + str(
                            person_record[7])

                        pdf.multi_cell(200, 10, stringPerson)
                    pdf.output(fileName, 'F')

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))

            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")

