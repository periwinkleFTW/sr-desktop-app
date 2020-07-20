from os import path as osPath
from sqlite3 import connect as sq3Connect
from sqlite3 import Row as sq3Row

from PyQt5.QtCore    import QSettings
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import QFileDialog, QMessageBox

############################## SQLite3 Database Class ##############################
# This handles everything pertinent to the SQLite3 Database and presents API 
# references as needed by the external.  Note currently as designed this Class can
# not be put into a Sub-Thread as it uses QtWidgets, Properties, direct API function
# calls all of which are not compatible with Threading a Class
#
class MyDatabase:
    def __init__(self, SourceDbase):
        self.__SQLDef = ''

      # Establish Full Path to Database
        DbaseFilePath = ''
        if len(SourceDbase) > 0 and osPath.isfile(SourceDbase):
            DbaseFilePath = SourceDbase
        else:
            DbaseFilePath = str(QSettings('CompanyName','ProjectName').value('LastProject'))

        if len(DbaseFilePath) == 0:
            DbaseFilePath = self.SetDatabase()
        
        # If DbaseFilePath is still empty the user has chosen not to supply a valid *.sql abort the program 
        if len(DbaseFilePath) < 1: 
            sysExit()

        QSettings('CompanyName','ProjectName').setValue('LastProject', DbaseFilePath)
        self.__dbasePathName = DbaseFilePath

  # Internal Database Functionality ************************************************
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
        filter  = "sql(*.sql)"
        caption = "Please Select a Valid Project Database"
        path    = str(QSettings('CompanyName', 'ProjectName').value('LastProject'))
        if len(path) > 0:
            path = osPath.dirname(path)
        else:
            path = str(QDir.currentPath())

        IsProject = False
        dbContinue = True
        while dbContinue:
            FindProj = QFileDialog()
            FindProj.setModal(True)
            FindProj.setFixedSize(self.size())
            filePathName = FindProj.getOpenFileName(None, caption, path, filter)[0]

            # Is this a legitimate file
            if osPath.isfile(filePathName):
                filPthNam, fileExt = ntSplitext(filePathName)
                # Does it have a legitimate file extension
                if fileExt == '.sql':
                    IsProject = True

            if not IsProject:
                ValidMsg = QMessageBox()
                ValidMsg.setIcon(QMessageBox.Warning)
                ValidMsg.setWindowTitle('CompanyName - ProjectName Project')
                ValidMsg.setText('This is not a Valid Project Database would you like to try again?')
                ValidMsg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
                ValidMsg.setDefaultButton(QMessageBox.No)
                ValidMsg.setWindowFlags(Qt.WindowStaysOnTopHint)

                MsgReply = ValidMsg.exec_()
                if MsgReply == QMessageBox.No:
                    dbContinue = False
                    filePathName = ''
            else:
                QSettings('CompanyName','ProjectName').setValue("LastProjectPath",osPath.dirname(filePathName))
                dbContinue = False

        return filePathName
       
    @dbSQLStr.setter
    def dbSQLStr(self, value):
        self.__SQLDef = value
    
    def OpenConn(self):
        try:
            self.dbConn = sq3Connect(self.__dbasePathName)
            # This uses the native structure that mostly resembles a Recordset/Dictionary
            self.dbConn.row_factory = sq3Row
            # This removes the unicode prefix from a string
            self.dbConn.text_factory = str
            self.dbCrsr = self.dbConn.cursor()
        except Exception as err:
            print("ERROR : OpenConn :",err)
            print("Database : [" + self.__dbasePathName + "]")
            sysExit()

    def CloseConn(self):
        self.dbConn.close()

    def dbQuery(self):
        try:
            self.OpenConn()
            self.dbCrsr.execute(self.dbSQLStr)
            return self.dbCrsr.fetchall()
        except Exception as err:
            print("ERROR : dbQuery :",err)
            print(self.dbSQLStr)
            sysExit()
        finally:
            self.CloseConn()

    def dbExecute(self):
        try:
            self.OpenConn()
            self.dbCrsr.execute(self.dbSQLStr)
            self.dbConn.commit()
        except Exception as err:
            print("ERROR : dbExecute :",err)
            print("Query : ",self.dbSQLStr)
            sysExit()
        finally:
            self.CloseConn()

# ********************************************************************************* 
# Pre-Defined Stored Procedures
# ********************************************************************************* 

# Everything from here on down should be viewed as a Stored Procedure since sqlite3 
# does not support Stored Procedure this Class can be viewed as an Sqlite3 extender 
#
# The naming of the Stored Procedures should be applicable in some way to what they
# are doing with what such as GetAddress would retrieve Address data from the 
# database and SaveAddress and SaveAddress would save Address data to the database
#
    def StoredProcedure_01(self):
        self.dbSQLStr = 'SELECT Field1, Field2  FROM tblTableName1 '
        self.dbSQLStr += 'ORDER BY Field2'

        Sq3RecordObj = self.dbQuery()

        self.ReturnRequestedData(ReqId, Sq3RecordObj, 1)
        
        return Sq3RecordObj

    def StoredProcedure_02(self):
        self.dbSQLStr = 'SELECT Field1, Field2  FROM tblTableName2 '
        self.dbSQLStr += 'ORDER BY Field2'

        Sq3RecordObj = self.dbQuery()

        self.ReturnRequestedData(ReqId, Sq3RecordObj, 1)
        
        return Sq3RecordObj

    def StoredProcedure_03(self, DataToSave):
      # Note DataToSave in this instances is a Dictionary of {ItemId:ItemValue, etc...}
        cnt = 0
        self.dbSQLStr = 'INSERT INTO tblTableName1 VALUES '
        for ItemId in DataToSave:
            if cnt > 0:
                self.dbSQLStr += ', '
            cnt += 1
            ItemValue = DataToSave[ItemId]
            self.dbSQLStr += '(' + str(ItemId) + ', "' + ItemValue +'")' 
        self.dbSQLStr += ';'
        self.dbExecute()
