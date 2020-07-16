import sqlite3
from sqlite3 import Error
from os import path as osPath


from PySide2.QtCore    import QSettings
from PySide2.QtGui     import *
from PySide2.QtWidgets import QFileDialog, QMessageBox


class MyDatabase:
    def __init__(self, SourceDbase):
        self.__SQLDef = ''

        # Establish Full Path to Database
        DbaseFilePath = ''
        if len(SourceDbase) > 0 and osPath.isfile(SourceDbase):
            DbaseFilePath = SourceDbase
        else:
            DbaseFilePath = str(QSettings('CompanyName', 'UserName').value('LastProject'))

        if len(DbaseFilePath) == 0:
            DbaseFilePath = self.SetDatabase()

        # If DbaseFilePath is still empty the user has chosen not to supply a valid *.sql abort the program
        if len(DbaseFilePath) < 1:
            sysExit()

        QSettings('CompanyName', 'UserName').setValue('LastProject', DbaseFilePath)
        self.__dbasePathName = DbaseFilePath


    # Internal functionality
    @property
    def dbName(self):
        return self.__dbasePathName

    @dbName.setter
    def dbName(self, value):
        self.__dbasePathName = value

    @property
    def dbSQLStr(self):
        return self.__SQLDef

    def SetDatabase(self):
        filter = "sql(*.sql)"
        caption = "Please select a valid project Database"
        path = str(QSettings())






# class Database:
#     def __init__(self, db):
#         self.conn = self.create_connection(db)
#         self.cur = self.conn.cursor()
#
#         self.sqlCreatePeopleTable = "CREATE TABLE IF NOT EXISTS people (" \
#                                     "person_id INTEGER PRIMARY KEY AUTOINCREMENT," \
#                                     "person_first_name TEXT," \
#                                     "person_last_name TEXT," \
#                                     "person_title TEXT," \
#                                     "person_phone TEXT," \
#                                     "person_email TEXT," \
#                                     "person_location TEXT," \
#                                     "person_empl_type TEXT" \
#                                     ")"
#         self.sqlCreateFacilitiesTable = "CREATE TABLE IF NOT EXISTS facilities (" \
#                                         "facility_id INTEGER PRIMARY KEY AUTOINCREMENT, " \
#                                         "facility_name TEXT, " \
#                                         "facility_location TEXT, " \
#                                         "facility_phone TEXT NOT NULL, " \
#                                         "facility_email TEXT NOT NULL, " \
#                                         "facility_supervisor TEXT NOT NULL" \
#                                         ")"
#         self.sqlCreateIssuesTable = "CREATE TABLE IF NOT EXISTS issues (" \
#                                     "issue_id INTEGER PRIMARY KEY AUTOINCREMENT," \
#                                     "issue_date TEXT," \
#                                     "issue_priority TEXT," \
#                                     "issue_observer TEXT," \
#                                     "issue_team TEXT," \
#                                     "issue_inspection TEXT," \
#                                     "issue_theme TEXT," \
#                                     "issue_facility TEXT," \
#                                     "issue_fac_supervisor TEXT," \
#                                     "issue_spec_loc TEXT," \
#                                     "issue_insp_dept TEXT," \
#                                     "issue_insp_contr TEXT," \
#                                     "issue_insp_subcontr TEXT," \
#                                     "issue_deadline DATETIME, " \
#                                     "status TEXT DEFAULT 'Open', " \
#                                     "created_on DATETIME, " \
#                                     "closed_on DATETIME" \
#                                     ")"
#
#         if self.conn is not None:
#             self.create_table(self.conn, self.sqlCreateIssuesTable)
#             self.create_table(self.conn, self.sqlCreatePeopleTable)
#             self.create_table(self.conn, self.sqlCreateFacilitiesTable)
#
#         else:
#             print("Error! Cannot establish database connection")
#
#         #######################################################################
#         # This block is used for populating db with dummy data from csv
#         # Column names should match those in the table
#         # *******************************
#         # df1 = pandas.read_csv("data/person-data.csv", sep="|",)
#         # df1.to_sql('people', self.conn, if_exists='append', index=False)
#         # df2 = pandas.read_csv("data/facility-data.csv", sep="|")
#         # df2.to_sql('facilities', self.conn, if_exists='append', index=False)
#         #######################################################################
#
#     def create_connection(self, db_file):
#         conn = None
#         try:
#             conn = sqlite3.connect(db_file)
#             return conn
#         except Error as e:
#             print(e)
#
#         return conn
#
#     def create_table(self, conn, create_table_sql):
#         try:
#             cur = conn.cursor()
#             cur.execute(create_table_sql)
#         except Error as e:
#             print(e)


