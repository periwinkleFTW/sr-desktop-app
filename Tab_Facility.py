
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton
from PySide2.QtWidgets import QRadioButton, QHBoxLayout, QVBoxLayout
from PySide2.QtWidgets import QTableWidgetItem, QTableWidget, QGroupBox, QMessageBox
from PySide2.QtWidgets import QHeaderView, QTableView, QAbstractItemView, QCheckBox, QFileDialog
from PySide2.QtCore import Qt, Slot




import csv
import xlsxwriter
import datetime
import styles
from backend import Database
from add_facility import AddFacility
from display_facility import DisplayFacility
from pdf_generator import PDF

db = Database("sr-data.db")

class FacilityTab(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.Parent = parent

        self.FcltyTitle = 'FACILITIES'

        self.UI()

    @property
    def Title(self):
        return self.FcltyTitle

    def UI(self):
        self.widgets()
        self.layouts()
        self.funcDisplayFacilities()

    def widgets(self):
        # Facilities widgets ###########################################################
        # Top layout (search facilities) widgets
        self.searchFacilitiesText = QLabel("Search facilities: ")
        self.searchFacilitesEntry = QLineEdit()
        self.searchFacilitesEntry.setPlaceholderText("Search facilities..")
        self.searchFacilitiesBtn = QPushButton("Search")
        self.searchFacilitiesBtn.clicked.connect(self.funcSearchFacilities)

        # Middle layout (list people) widgets with radio buttons
        self.allFacilitiesRadioBtn = QRadioButton("All facilities")
        self.withOngoingIssuesFacilitiesRadioBtn = QRadioButton("With ongoing issues")
        self.withLateIssuesRadioBtn = QRadioButton("With late issues")
        self.listFacilitiesBtn = QPushButton("List facilities")

        # Bottom layout widget, a table showing people
        self.facilitiesTable = QTableWidget()
        self.facilitiesTable.verticalHeader().hide()
        self.facilitiesTable.setSortingEnabled(True)
        self.facilitiesTable.setShowGrid(False)
        self.facilitiesTable.verticalHeader().setDefaultSectionSize(40)
        self.facilitiesTable.setColumnCount(11)
        # self.peopleTable.setColumnHidden(0, True)
        self.facilitiesTable.setHorizontalHeaderItem(0, QTableWidgetItem(""))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.facilitiesTable.setHorizontalHeaderItem(1, QTableWidgetItem("ID"))
        self.facilitiesTable.setHorizontalHeaderItem(2, QTableWidgetItem("Name"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(3, QTableWidgetItem("Location"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(4, QTableWidgetItem("Phone"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(5, QTableWidgetItem("Email"))
        self.facilitiesTable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.facilitiesTable.setHorizontalHeaderItem(6, QTableWidgetItem("Supervisor"))
        self.facilitiesTable.setHorizontalHeaderItem(7, QTableWidgetItem("Ongoing issues"))
        self.facilitiesTable.setHorizontalHeaderItem(8, QTableWidgetItem("Late issues"))
        self.facilitiesTable.setHorizontalHeaderItem(9, QTableWidgetItem("Total issues"))
        self.facilitiesTable.setHorizontalHeaderItem(10, QTableWidgetItem("Total inspections"))

        # Double clicking a row opens a window with person details
        self.facilitiesTable.doubleClicked.connect(self.funcSelectedFacility)

        # Buttons for actions on selected facilities
        self.addFacility = QPushButton("Add facility")
        self.addFacility.clicked.connect(self.funcAddFacility)
        self.viewFacility = QPushButton("View/Edit facility")
        self.viewFacility.clicked.connect(self.funcSelectedFacility)
        self.deleteFacility = QPushButton("Delete facility")
        self.deleteFacility.clicked.connect(self.funcDeleteFacility)
        self.exportFacilitiesCSVBtn = QPushButton("Export CSV")
        self.exportFacilitiesCSVBtn.clicked.connect(self.funcFacilitiesToCSV)
        self.exportFacilitiesXSLXBtn = QPushButton("Export XLSX")
        self.exportFacilitiesXSLXBtn.clicked.connect(self.funcFacilitiesToXLSX)
        self.exportFacilitiesPDFBtn = QPushButton("Export PDF")
        self.exportFacilitiesPDFBtn.clicked.connect(self.funcFacilitiesToPdf)


    def layouts(self):
        # Facilities layouts ###########################################################
        self.facilitiesMainLayout = QVBoxLayout()
        self.facilitiesMainTopLayout = QHBoxLayout()
        self.facilitiesTopLeftLayout = QHBoxLayout()
        self.facilitiesTopRightLayout = QHBoxLayout()

        self.facilitiesMainBottomLayout = QHBoxLayout()
        self.facilitiesBottomRightLayout = QVBoxLayout()
        self.facilitiesBottomLeftLayout = QHBoxLayout()

        # Groupboxes allows customization using CSS-like syntax

        self.facilitiesTopLeftGroupBox = QGroupBox()
        self.facilitiesTopRightGroupBox = QGroupBox()
        self.facilitiesTopGroupBox = QGroupBox()


        self.facilitiesBottomGroupBox = QGroupBox()
        self.facilitiesBottomLeftGroupBox = QGroupBox()
        self.facilitiesBottomRightGroupBox = QGroupBox()
        self.facilitiesBottomRightGroupBox.setStyleSheet('QGroupBox {margin-top: 0px;}')
        self.facilitiesBottomRightGroupBoxFiller = QGroupBox()
        self.facilitiesBottomRightGroupBoxFiller.setStyleSheet(styles.groupBoxFillerStyle())

        # Top layout (search box) widgets
        self.facilitiesTopLeftLayout.addWidget(self.searchFacilitiesText, 10)
        self.facilitiesTopLeftLayout.addWidget(self.searchFacilitesEntry, 30)
        self.facilitiesTopLeftLayout.addWidget(self.searchFacilitiesBtn, 10)
        self.facilitiesTopLeftGroupBox.setLayout(self.facilitiesTopLeftLayout)

        # layout (list box) widgets
        self.facilitiesTopRightLayout.addWidget(self.allFacilitiesRadioBtn)
        self.facilitiesTopRightLayout.addWidget(self.withOngoingIssuesFacilitiesRadioBtn)
        self.facilitiesTopRightLayout.addWidget(self.withLateIssuesRadioBtn)
        self.facilitiesTopRightLayout.addWidget(self.listFacilitiesBtn)
        self.facilitiesTopRightGroupBox.setLayout(self.facilitiesTopRightLayout)

        self.facilitiesMainTopLayout.addWidget(self.facilitiesTopLeftGroupBox)
        self.facilitiesMainTopLayout.addWidget(self.facilitiesTopRightGroupBox)

        # Bottom layout (table with facilities) widgets
        # Bottom left layout with table
        self.facilitiesBottomLeftLayout.addWidget(self.facilitiesTable)
        self.facilitiesBottomLeftGroupBox.setLayout(self.facilitiesBottomLeftLayout)

        # Bottom right layout with buttons
        self.facilitiesBottomRightLayout.addWidget(self.addFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.viewFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.deleteFacility, 5)
        self.facilitiesBottomRightLayout.addWidget(self.facilitiesBottomRightGroupBoxFiller, 70)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesCSVBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesXSLXBtn, 5)
        self.facilitiesBottomRightLayout.addWidget(self.exportFacilitiesPDFBtn, 5)
        self.facilitiesBottomRightGroupBox.setLayout(self.facilitiesBottomRightLayout)

        self.facilitiesMainBottomLayout.addWidget(self.facilitiesTable, 90)
        self.facilitiesMainBottomLayout.addWidget(self.facilitiesBottomRightGroupBox, 10)

        self.facilitiesMainLayout.addLayout(self.facilitiesMainTopLayout, 10)
        self.facilitiesMainLayout.addLayout(self.facilitiesMainBottomLayout, 90)

        self.setLayout(self.facilitiesMainLayout)

    @Slot()
    def funcAddFacility(self):
        self.newFacility = AddFacility(self)
        self.newFacility.setObjectName("add_facility_popup")
        self.newFacility.setStyleSheet(styles.addPopups())

    @Slot()
    def funcDisplayFacilities(self):
        for i in reversed(range(self.facilitiesTable.rowCount())):
            self.facilitiesTable.removeRow(i)

        cur = db.cur
        facilities = cur.execute("SELECT * FROM facilities")

        for row_data in facilities:
            row_number = self.facilitiesTable.rowCount()
            self.facilitiesTable.insertRow(row_number)
            # Add checkboxes to the table
            qwidget = QWidget()
            checkbox = QCheckBox()
            checkbox.setCheckState(Qt.Unchecked)
            qhboxlayout = QHBoxLayout(qwidget)
            qhboxlayout.addWidget(checkbox)
            qhboxlayout.setAlignment(Qt.AlignCenter)
            self.facilitiesTable.setCellWidget(row_number, 0, qwidget)
            self.facilitiesTable.setItem(row_number, 0, QTableWidgetItem(row_number))

            for column_number, data in enumerate(row_data, start=1):
                if column_number == 1:
                    self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem("FCL#" + str(data)))
                else:
                    self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.facilitiesTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.facilitiesTable.setSelectionBehavior(QTableView.SelectRows)

    @Slot()
    def funcFacilitiesCheckBox(self):
        checked_list = []
        for i in range(self.facilitiesTable.rowCount()):
            if self.facilitiesTable.cellWidget(i, 0).findChild(type(QCheckBox())).isChecked():
                item = self.facilitiesTable.item(i, 1).text()
                checked_list.append(item.lstrip("FCL#"))
        return checked_list

    @Slot()
    def funcSelectedFacility(self):
        self.displayFacility = DisplayFacility(self)
        self.displayFacility.show()

    @Slot()
    def funcDeleteFacility(self):
        indices = self.funcFacilitiesCheckBox()

        mbox = QMessageBox.question(self, "Warning", "Are you sure you want to delete this facility?",
                                    QMessageBox.Yes | QMessageBox.Cancel, QMessageBox.Cancel)

        if (mbox == QMessageBox.Yes):
            if indices:
                try:
                    for index in range(len(indices)):
                        query = "DELETE FROM facilities WHERE facility_id = ?"

                        db.cur.execute(query, (indices[index],))
                        db.conn.commit()

                    QMessageBox.information(self, "Info", "Facilites were deleted")
                    self.funcDisplayFacilities()
                except:
                    QMessageBox.information(self, "Info", "No changes made")
            else:
                row = self.facilitiesTable.currentRow()
                facilityId = self.facilitiesTable.item(row, 0).text()
                facilityId = facilityId.lstrip("FCL#")
                try:
                    query = "DELETE FROM facilities WHERE facility_id = ?"

                    db.cur.execute(query, (facilityId,))
                    db.conn.commit()

                    QMessageBox.information(self, "Info", "Facility was deleted")
                    self.funcDisplayFacilities()
                except:
                    QMessageBox.information(self, "Info", "No changes made")
        self.displayFacility.close()

    @Slot()
    def funcSearchFacilities(self):
        value = self.searchFacilitesEntry.text()
        if value == "":
            QMessageBox.information(self, "Warning", "Search string cannot be empty")
            self.displayFacilities()
        else:
            # Erase search entry
            self.searchFacilitesEntry.setText("")
            try:
                query = "SELECT * FROM facilities WHERE " \
                        "facility_id LIKE ? " \
                        "OR facility_name LIKE ?" \
                        "OR facility_location LIKE ?" \
                        "OR facility_phone LIKE ?" \
                        "OR facility_email LIKE ?" \
                        "OR facility_supervisor LIKE ?"
                results = db.cur.execute(query, ('%' + value + '%', '%' + value + '%', '%' + value + '%',
                                                 '%' + value + '%', '%' + value + '%', '%' + value + '%')).fetchall()
                if results == []:
                    QMessageBox.information(self, "Info", "Nothing was found")
                    self.funcDisplayFacilities()
                else:
                    for i in reversed(range(self.facilitiesTable.rowCount())):
                        self.facilitiesTable.removeRow(i)

                    for row_data in results:
                        row_number = self.facilitiesTable.rowCount()
                        self.facilitiesTable.insertRow(row_number)
                        # Add checkboxes to the table
                        qwidget = QWidget()
                        checkbox = QCheckBox()
                        checkbox.setCheckState(Qt.Unchecked)
                        qhboxlayout = QHBoxLayout(qwidget)
                        qhboxlayout.addWidget(checkbox)
                        qhboxlayout.setAlignment(Qt.AlignCenter)
                        self.facilitiesTable.setCellWidget(row_number, 0, qwidget)
                        self.facilitiesTable.setItem(row_number, 0, QTableWidgetItem(row_number))
                        for column_number, data in enumerate(row_data, start=1):
                            if column_number == 1:
                                self.facilitiesTable.setItem(row_number, column_number,
                                                         QTableWidgetItem("FCL#" + str(data)))
                            else:
                                self.facilitiesTable.setItem(row_number, column_number, QTableWidgetItem(str(data)))
            except:
                QMessageBox.information(self, "Info", "Cannot access database")

    @Slot()
    def funcFacilitiesToCSV(self):
        indices = self.funcFacilitiesCheckBox()
        # Check if there are any selected items
        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/FacilitiesCSV" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".csv",
                    "CSV files (*.csv)")
                if fileName:
                    with open(fileName, "w") as csv_file:
                        csv_writer = csv.writer(csv_file, delimiter="|")
                        # Setting cursor on the correct table
                        db.cur.execute("SELECT * FROM facilities")
                        # Get headers
                        csv_writer.writerow([i[0] for i in db.cur.description])
                        for index in indices:
                            query = "SELECT * FROM facilities WHERE facility_id=?"
                            facility_record = db.cur.execute(query, (index,)).fetchone()
                            csv_writer.writerow(facility_record)

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))
            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select facilities to export")

    @Slot()
    def funcFacilitiesToXLSX(self):
        indices = self.funcFacilitiesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/FacilitiesXLSX" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".xlsx",
                    "Excel files (*.xlsx)")
                if fileName:
                    db.cur.execute("SELECT * FROM facilities")

                    workbook = xlsxwriter.Workbook(fileName)
                    worksheet = workbook.add_worksheet("Facilities")

                    # Create header row
                    col = 0
                    for value in db.cur.description:
                        worksheet.write(0, col, value[0])
                        col += 1

                    # Write date to xlsx file
                    row_number = 1
                    for index in range(len(indices)):
                        query = "SELECT * FROM facilities WHERE facility_id=?"
                        facility_record = db.cur.execute(query, (indices[index],)).fetchone()
                        for i, value in enumerate(facility_record):
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
    def funcFacilitiesToPdf(self):
        indices = self.funcFacilitiesCheckBox()

        if indices:
            try:
                date = datetime.datetime.now()

                # Get file location and add timestamp to when it was created to the filename
                fileName, _ = QFileDialog.getSaveFileName(
                    self, "Save as...", "~/FacilitiesPDF" + "{:%d%b%Y_%Hh%Mm}".format(date) + ".pdf",
                    "PDF files (*.pdf)")

                if fileName:
                    pdf = PDF()
                    pdf.add_page()
                    pdf.set_font('Arial', 'B', 13)

                    for index in range(len(indices)):
                        query = "SELECT * FROM facilities WHERE facility_id=?"
                        facility_record = db.cur.execute(query, (indices[index],)).fetchone()

                        # This string allows for text formatting in the pdf, easy to implement and test
                        stringFacility = "\nFacility id: " + str(facility_record[0]) + "\nFacility name: " + str(facility_record[1]) + \
                                      "\nLocation: " + str(facility_record[2]) + "\nPhone: " + str(
                            facility_record[3]) + \
                                      "\nEmail: " + str(facility_record[4]) + "\nSupervisor: " + str(
                            facility_record[5])

                        pdf.multi_cell(200, 10, stringFacility)
                    pdf.output(fileName, 'F')

                    QMessageBox.information(self, "Info", "Data exported successfully into {}".format(fileName))

            except:
                QMessageBox.information(self, "Info", "Export failed")
        else:
            QMessageBox.information(
                self, "Info", "Nothing selected for export\nUse checkboxes to select issues to export")