from PySide2.QtWidgets import QFileDialog, QMessageBox

from backend import Database

import csv
import datetime


class CSV():
    def __init__(self, parent, entity, indices):
        self.Parent = parent
        self.db = Database("sr-data.db")

        self.date = datetime.datetime.now()

        self.indices = indices
        self.entity = entity

        if entity == "issues":
            self.fileName, _ = QFileDialog.getSaveFileName(
                self.Parent, "Save as...", "~/IssuesCSV" + "{:%d%b%Y_%Hh%Mm}".format(self.date) + ".csv",
                "CSV files (*.csv)")

            # Set cursor location on correct table to get column names
            self.db.cur.execute("SELECT * FROM issues")

            self.query = "SELECT * FROM issues WHERE issue_id=?"

            # This variable controls number of columns to be fetched
            self.stop = 17

        elif entity == "people":
            self.fileName, _ = QFileDialog.getSaveFileName(
                self.Parent, "Save as...", "~/PeopleCSV" + "{:%d%b%Y_%Hh%Mm}".format(self.date) + ".csv",
                "CSV files (*.csv)")

            # Set cursor location on correct table to get column names
            self.db.cur.execute("SELECT * FROM people")

            self.query = "SELECT * FROM people WHERE person_id=?"

            # This variable controls number of columns to be fetched
            self.stop = 8

        elif entity == "facilities":
            self.fileName, _ = QFileDialog.getSaveFileName(
                self.Parent, "Save as...", "~/FacilitiesCSV" + "{:%d%b%Y_%Hh%Mm}".format(self.date) + ".csv",
                "CSV files (*.csv)")

            # Set cursor location on correct table to get column names
            self.db.cur.execute("SELECT * FROM facilities")

            self.query = "SELECT * FROM facilities WHERE facility_id=?"

            # This variable controls number of columns to be fetched
            self.stop = 6
        else:
            QMessageBox.information(self.Parent, "Info", "Something went wrong during generation of CSV file...")

        self.generateCsv()

    def generateCsv(self):
        try:
            if self.fileName:
                with open(self.fileName, "w") as csv_file:
                    csv_writer = csv.writer(csv_file, delimiter="|")
                    csv_writer.writerow([i[0] for i in self.db.cur.description[:self.stop]])
                    for index in self.indices:
                        record = self.db.cur.execute(self.query, (index,)).fetchone()
                        csv_writer.writerow(record[:self.stop])

                QMessageBox.information(self.Parent, "Info", "Data exported successfully into {}".format(self.fileName))
        except:
            QMessageBox.information(self.Parent, "Info", "Export failed")
