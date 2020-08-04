try:
    from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, \
        QFormLayout, QFrame, QMessageBox
    from PySide2.QtGui import QIcon, QPixmap
    from PySide2.QtCore import Qt
except:
    from PyQt.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QComboBox, QVBoxLayout, \
        QFormLayout, QFrame, QMessageBox
    from PyQt.QtGui import QIcon, QPixmap
    from PyQt.QtCore import Qt

from backend import Database

db = Database("sr-data.db")

class DisplayPerson(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("View person")
        self.setWindowIcon(QIcon("assets/icons/logo-dark.png"))
        self.setGeometry(450, 150, 750, 650)

        self.Parent = parent

        self.UI()
        self.show()

    def UI(self):
        self.personDetails()
        self.widgets()
        self.layouts()

    def personDetails(self):
        row = self.Parent.peopleTable.currentRow()
        personId = self.Parent.peopleTable.item(row, 2).text()

        # Adding prefixes to tables changed the format of the Id from and integer to a string PRN#+id
        # Following code strips letters
        personId = personId.lstrip("PRN#")

        query = "SELECT * FROM people WHERE person_id=?"

        person = db.cur.execute(query, (personId,)).fetchone()

        self.id = person[0]
        self.firstName = person[1]
        self.lastName = person[2]
        self.title = person[3]
        self.phone = person[4]
        self.email = person[5]
        self.location = person[6]
        self.emplType = person[7]

    def widgets(self):
        # Top layout widgets
        self.personImg = QLabel()
        self.img = QPixmap('assets/icons/logo-dark.png')
        self.personImg.setPixmap(self.img)
        self.personImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("Display person")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.idEntry = QLabel(str(self.id))
        self.firstNameEntry = QLineEdit()
        self.firstNameEntry.setText(self.firstName)
        self.lastNameEntry = QLineEdit()
        self.lastNameEntry.setText(self.lastName)
        self.titleEntry = QLineEdit()
        self.titleEntry.setText(self.title)
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setText(self.phone)
        self.emailEntry = QLineEdit()
        self.emailEntry.setText(self.email)
        self.locationEntry = QLineEdit()
        self.locationEntry.setText(self.location)

        emplTypes = ["Employee", "Contractor", "Subcontractor"]
        self.employmentTypeEntry = QComboBox()
        self.employmentTypeEntry.addItems(emplTypes)
        self.employmentTypeEntry.setCurrentText(self.emplType)

        self.updateBtn = QPushButton("Update")
        self.updateBtn.clicked.connect(self.updatePerson)
        self.deleteBtn = QPushButton("Delete")
        self.deleteBtn.clicked.connect(self.Parent.funcDeletePerson)

    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.bottomLayout = QFormLayout()
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets
        self.topLayout.addWidget(self.titleText)
        self.topLayout.addWidget(self.personImg)
        self.topFrame.setLayout(self.topLayout)

        self.bottomLayout.addRow("ID: ", self.idEntry)
        self.bottomLayout.addRow("First name: ", self.firstNameEntry)
        self.bottomLayout.addRow("Last name: ", self.lastNameEntry)
        self.bottomLayout.addRow("Title: ", self.titleEntry)
        self.bottomLayout.addRow("Phone: ", self.phoneEntry)
        self.bottomLayout.addRow("Email: ", self.emailEntry)
        self.bottomLayout.addRow("Location: ", self.locationEntry)
        self.bottomLayout.addRow("Employment type: ", self.employmentTypeEntry)
        self.bottomLayout.addRow("", self.updateBtn)
        self.bottomLayout.addRow("", self.deleteBtn)
        self.bottomFrame.setLayout(self.bottomLayout)

        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    def updatePerson(self):
        row = self.Parent.peopleTable.currentRow()
        personId = self.Parent.peopleTable.item(row, 2).text()
        personId = personId.lstrip("PRN#")

        firstName = self.firstNameEntry.text()
        lastName = self.lastNameEntry.text()
        title = self.titleEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        location = self.locationEntry.text()
        emplType = self.employmentTypeEntry.currentText()

        if (firstName and lastName and title and phone and email and emplType != ""):
            try:
                query = "UPDATE people SET person_first_name=?, person_last_name=?, person_title=?," \
                        "person_phone=?, person_email=?, person_location=?, person_empl_type=? WHERE person_id=?"
                db.cur.execute(query, (firstName, lastName, title, phone, email, location, emplType, personId))
                db.conn.commit()
                QMessageBox.information(self, "Info", "Person info updated")
            except:
                QMessageBox.information(self, "Info", "No changes made")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")

        self.Parent.funcDisplayPeople()
        self.close()

