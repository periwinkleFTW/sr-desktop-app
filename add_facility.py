import random
import string
from datetime import datetime
from os import path as osPath
from shutil import copy2 as ShCopy2
from PIL import Image

from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QFrame, QFormLayout, QMessageBox, QSpacerItem, QSizePolicy, QFileDialog
from PySide2.QtGui import QPixmap, QIcon
from PySide2.QtCore import Qt, Slot


import backend

db = backend.Database("sr-data.db")

defaultImg = "assets/icons/logo-dark.png"

class AddFacility(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("Add facility")
        self.setWindowIcon(QIcon("assets/icons/icon.ico"))
        self.setGeometry(450, 150, 400, 250)
        #self.setFixedSize(self.size())

        self.Parent = parent

        self.filePathName = ""

        self.UI()
        self.show()

    def UI(self):
        self.widgets()
        self.layouts()

    def widgets(self):
        # Top layout widgets
        self.addFacilityImg = QLabel()
        self.img = QPixmap('assets/icons/add-facility.png')
        self.addFacilityImg.setPixmap(self.img)
        self.addFacilityImg.setAlignment(Qt.AlignCenter)
        self.titleText = QLabel("ADD FACILITY")
        self.titleText.setObjectName("add_fcl_title_txt")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.facilityInfoTitleText = QLabel("Facility info")
        self.facilityInfoTitleText.setAlignment(Qt.AlignCenter)
        self.facilityIdEntry = QLineEdit()
        self.facilityNameEntry = QLineEdit()
        self.facilityLocationEntry = QLineEdit()
        self.facilityPhoneEntry = QLineEdit()
        self.facilityEmailEntry = QLineEdit()
        self.facilitySupervisorEntry = QLineEdit()

        self.attachPhotoBtn = QPushButton("Attach photo")
        self.attachPhotoBtn.clicked.connect(self.funcAttachFiles)

        self.addFacilityBtn = QPushButton("Add facility")
        self.addFacilityBtn.clicked.connect(self.addFacility)

        self.cancelBtn = QPushButton("Cancel")
        self.cancelBtn.clicked.connect(self.closeWindow)


    def layouts(self):
        self.mainLayout = QVBoxLayout()
        self.topLayout = QHBoxLayout()
        self.bottomLayout = QFormLayout()
        self.bottomLayout.setVerticalSpacing(20)
        self.bottomBtnLayout = QHBoxLayout()

        # Put elements into frames for visual distinction
        self.topFrame = QFrame()
        self.bottomFrame = QFrame()

        # Add widgets to top layout
        # self.topLayout.addWidget(self.addFacilityImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        self.bottomLayout.addWidget(self.facilityInfoTitleText)
        self.bottomLayout.addRow(QLabel("Facility name: "), self.facilityNameEntry)
        self.bottomLayout.addRow(QLabel("Location: "), self.facilityLocationEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.facilityPhoneEntry)
        self.bottomLayout.addRow(QLabel("Email: "), self.facilityEmailEntry)
        self.bottomLayout.addRow(QLabel("Facility supervisor: "), self.facilitySupervisorEntry)
        self.bottomLayout.addRow(QLabel(""), self.attachPhotoBtn)

        self.bottomBtnLayout.addWidget(self.cancelBtn)
        self.bottomBtnLayout.addItem(QSpacerItem(200, 5, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.bottomBtnLayout.addWidget(self.addFacilityBtn)

        self.bottomBtnLayout.setAlignment(Qt.AlignBottom)

        self.bottomLayout.addRow(self.bottomBtnLayout)

        self.bottomFrame.setLayout(self.bottomLayout)

        # Add frames to main layout
        self.mainLayout.addWidget(self.topFrame)
        self.mainLayout.addWidget(self.bottomFrame)

        self.setLayout(self.mainLayout)

    @Slot()
    def closeWindow(self):
        self.close()

    @Slot()
    def addFacility(self):
        # If user selected a file to attach, rename the file and copy it to media folder
        if self.filePathName != "":
            self.newFilePath = ShCopy2(self.filePathName, self.attachedFilePath)

            im = Image.open(self.filePathName)

            im_resized = self.crop_max_square(im).resize((800, 800), Image.LANCZOS)
            im_resized.save(self.attachedResizedFilePath)
        else:
            self.attachedFilePath = ""
            self.attachedResizedFilePath = ""

        name = self.facilityNameEntry.text()
        location = self.facilityLocationEntry.text()
        phone = self.facilityPhoneEntry.text()
        email = self.facilityEmailEntry.text()
        supervisor = self.facilitySupervisorEntry.text()

        if (name and location and phone and email and supervisor != ""):
            try:
                query = "INSERT INTO facilities (facility_name, facility_location, facility_phone, facility_email," \
                        "facility_supervisor) VALUES (?, ?, ?, ?, ?)"

                db.cur.execute(query, (name, location, phone, email, supervisor))
                db.conn.commit()
                QMessageBox.information(self, "Info", "Facility has been added")

                self.Parent.funcDisplayFacilities()
                self.close()
            except:
                QMessageBox.information(self, "Info", "Facility has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")


    @Slot()
    def funcAttachFiles(self):
        self.filePathName = QFileDialog.getOpenFileName(self, "Attach file...", "/",
                                                        "Image files (*.jpg, *.jpeg, *.png)")[0]

        if osPath.isfile(self.filePathName):
            fileName, fileExt = osPath.splitext(self.filePathName)

            if fileExt == '.jpg' or fileExt == '.jpeg' or fileExt == '.png':
                date = datetime.now()
                randomSuffix = "".join(random.choice(string.ascii_lowercase) for i in range(15))

                self.attachedFilePath = osPath.join("assets", "media", "facilities-media", "photos",
                                                     ("{:%d%b%Y_%Hh%Mm}".format(date) + randomSuffix + fileExt))
                self.attachedResizedFilePath = osPath.join("assets", "media", "facilities-media", "photos_resized",
                                                            ("{:%d%b%Y_%Hh%Mm}".format(date) + randomSuffix + "_resized" + fileExt))

                # self.attachedFilePath = "./assets/media/facilities-media/" + \
                #                         "{:%d%b%Y_%Hh%Mm}".format(date) + randomSuffix + fileExt

                QMessageBox.information(self, "Info", "File attached successfully")

            else:
                QMessageBox.information(self, "Info", "Wrong file type!")
        else:
            QMessageBox.information(self, "Info", "Something went wrong. Try again...")


    # Image processing functions
    @Slot()
    def crop_center(self, pil_img, crop_width, crop_height):
        img_width, img_height = pil_img.size

        fill_color = 'rgba(255, 255, 255, 1)'

        if pil_img.mode in ('RGBA', 'LA'):
            background = Image.new(pil_img.mode[:-1], pil_img.size, fill_color)
            background.paste(pil_img, pil_img.split()[-1])
            image = background

        return pil_img.crop(((img_width - crop_width) // 2,
                             (img_height - crop_height) // 2,
                             (img_width + crop_width) // 2,
                             (img_height + crop_height) // 2))

    # Crop the largest possible square from a rectangle
    @Slot()
    def crop_max_square(self, pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))



