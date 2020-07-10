import sys, os
from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QComboBox, QFrame, QFormLayout, QMessageBox
from PySide2.QtGui import QIcon, QPixmap
from PySide2.QtCore import Qt

import backend


db = backend.Database("sr-data.db")

defaultImg = "assets/icons/logo-dark.png"

class AddPerson(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("Add person")
        self.setWindowIcon(QIcon("assets/icons/icon.ico"))
        self.setGeometry(450, 150, 750, 650)
        #self.setFixedSize(self.size())

        self.Parent = parent

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.addPersonImg = QLabel()
        self.img = QPixmap('assets/icons/edit-item.png')
        self.addPersonImg.setPixmap(self.img)
        self.addPersonImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Add person")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.personInfoTitleText = QLabel("Person info")
        self.personInfoTitleText.setAlignment(Qt.AlignCenter)
        self.firstNameEntry = QLineEdit()
        self.lastNameEntry = QLineEdit()
        self.titleEntry = QLineEdit()
        self.phoneEntry = QLineEdit()
        self.emailEntry = QLineEdit()
        self.locationEntry = QLineEdit()

        emplTypes = ["Employee", "Contractor", "Subcontractor"]
        self.employmentTypeEntry = QComboBox()
        self.employmentTypeEntry.addItems(emplTypes)
        self.employmentTypeEntry.setEditable(True)

        self.attachPhotoBtn = QPushButton("Attach photo")

        self.addPersonBtn = QPushButton("Add person")
        self.addPersonBtn.clicked.connect(self.addPerson)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        # Put elements into frames for visual distinction
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets to top layout
        self.topLayout.addWidget(self.addPersonImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        self.bottomLayout.addWidget(self.personInfoTitleText)
        self.bottomLayout.addRow(QLabel("First name: "), self.firstNameEntry)
        self.bottomLayout.addRow(QLabel("Last name: "), self.lastNameEntry)
        self.bottomLayout.addRow(QLabel("Title: "), self.titleEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel("Email: "), self.emailEntry)
        self.bottomLayout.addRow(QLabel("Location: "), self.locationEntry)
        self.bottomLayout.addRow(QLabel("Employment type: "), self.employmentTypeEntry)
        self.bottomLayout.addRow(QLabel(""), self.attachPhotoBtn)
        self.bottomLayout.addRow(QLabel(""), self.addPersonBtn)

        self.bottomFrame.setLayout(self.bottomLayout)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)



    def addPerson(self):
        firstName = self.firstNameEntry.text()
        lastName = self.lastNameEntry.text()
        title = self.titleEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        location = self.locationEntry.text()
        emplType = self.employmentTypeEntry.currentText()

        if (firstName and lastName and title and phone and email and location and emplType != ""):
            try:
                query = "INSERT INTO people (person_first_name, person_last_name, person_title, person_phone," \
                        "person_email, person_location, person_empl_type) VALUES (?, ?, ?, ?, ?, ?, ?)"

                db.cur.execute(query, (firstName, lastName, title, phone, email, location, emplType))
                db.conn.commit()

                self.Parent.funcDisplayPeople()
                QMessageBox.information(self, "Info", "Member has been added")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Member has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")
