import random
import string
from datetime import datetime
from os import path as osPath
from shutil import copy2 as ShCopy2
from PIL import Image, ImageDraw, ImageFilter

from PySide2.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, \
    QComboBox, QFrame, QFormLayout, QMessageBox, QSpacerItem, QSizePolicy, QFileDialog
from PySide2.QtGui import QIcon, QPixmap, QPainter, QPalette, QPainterPath, QPen, QColor
from PySide2.QtCore import Qt, Slot

import backend

db = backend.Database("sr-data.db")

defaultImg = "assets/icons/logo-dark.png"


class AddPerson(QWidget):
    def __init__(self, parent):
        QWidget.__init__(self)
        self.setWindowTitle("Add person")
        self.setWindowIcon(QIcon("assets/icons/icon.ico"))
        self.setGeometry(450, 150, 400, 250)
        # self.setFixedSize(self.size())

        self.Parent = parent

        self.filePathName = ""

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
        self.titleText = QLabel("ADD PERSON")
        self.titleText.setObjectName("add_person_title_txt")
        self.titleText.setAlignment(Qt.AlignCenter)
        # Bottom layout widgets
        self.firstNameEntry = QLineEdit()
        self.firstNameEntry.setClearButtonEnabled(True)
        self.lastNameEntry = QLineEdit()
        self.lastNameEntry.setClearButtonEnabled(True)
        self.titleEntry = QLineEdit()
        self.titleEntry.setClearButtonEnabled(True)
        self.phoneEntry = QLineEdit()
        self.phoneEntry.setClearButtonEnabled(True)
        self.emailEntry = QLineEdit()
        self.emailEntry.setClearButtonEnabled(True)
        self.locationEntry = QLineEdit()
        self.locationEntry.setClearButtonEnabled(True)

        emplTypes = ["Employee", "Contractor", "Subcontractor"]
        self.employmentTypeEntry = QComboBox()
        self.employmentTypeEntry.addItems(emplTypes)
        self.employmentTypeEntry.setEditable(True)

        self.attachPhotoBtn = QPushButton("Attach photo")
        self.attachPhotoBtn.clicked.connect(self.funcAttachFiles)

        self.addPersonBtn = QPushButton("Add person")
        self.addPersonBtn.clicked.connect(self.addPerson)

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
        # self.topLayout.addWidget(self.addPersonImg)
        self.topLayout.addWidget(self.titleText)

        self.topFrame.setLayout(self.topLayout)

        # Add widgets to middle layout
        self.bottomLayout.addRow(QLabel("First name: "), self.firstNameEntry)
        self.bottomLayout.addRow(QLabel("Last name: "), self.lastNameEntry)
        self.bottomLayout.addRow(QLabel("Title: "), self.titleEntry)
        self.bottomLayout.addRow(QLabel("Phone: "), self.phoneEntry)
        self.bottomLayout.addRow(QLabel("Email: "), self.emailEntry)
        self.bottomLayout.addRow(QLabel("Location: "), self.locationEntry)
        self.bottomLayout.addRow(QLabel("Employment type: "), self.employmentTypeEntry)
        self.bottomLayout.addRow(QLabel(""), self.attachPhotoBtn)

        self.bottomBtnLayout.addWidget(self.cancelBtn)
        self.bottomBtnLayout.addItem(QSpacerItem(200, 5, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.bottomBtnLayout.addWidget(self.addPersonBtn)
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
    def addPerson(self):
        firstName = self.firstNameEntry.text()
        lastName = self.lastNameEntry.text()
        title = self.titleEntry.text()
        phone = self.phoneEntry.text()
        email = self.emailEntry.text()
        location = self.locationEntry.text()
        emplType = self.employmentTypeEntry.currentText()

        # If user selected a file to attach, rename the file and copy it to media folder
        # Else set the path variables to empty strings to avoid problems with db write
        if self.filePathName != "":
            self.newFilePath = ShCopy2(self.filePathName, self.attachedFilePath)

            im = Image.open(self.filePathName)

            im_resized = self.crop_max_square(im).resize((800, 800), Image.LANCZOS)
            im_resized.save(self.attachedResizedFilePath)

            im_square = self.crop_max_square(im).resize((60, 60), Image.LANCZOS)
            im_thumb = self.mask_circle_transparent(im_square, 60, 60, 2)

            im_thumb.save(self.attachedThumbnailPath)
        else:
            self.attachedFilePath = ""
            self.attachedResizedFilePath = ""
            self.attachedThumbnailPath = ""

        if (firstName and lastName and title and phone and email and location and emplType != ""):
            try:
                query = "INSERT INTO people (person_first_name, person_last_name, person_title, person_phone," \
                        "person_email, person_location, person_empl_type, photo_original_path, photo_resized_path, " \
                        "thumbnail_path) " \
                        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

                db.cur.execute(query, (firstName, lastName, title, phone, email, location, emplType,
                                       self.attachedFilePath, self.attachedResizedFilePath, self.attachedThumbnailPath))

                db.conn.commit()

                self.Parent.funcDisplayPeople()
                QMessageBox.information(self, "Info", "Member has been added")
                self.close()
            except:
                QMessageBox.information(self, "Info", "Member has not been added")
        else:
            QMessageBox.information(self, "Info", "Fields cannot be empty")

    @Slot()
    def funcAttachFiles(self):
        self.filePathName = QFileDialog.getOpenFileName(self, "Attach file...", "/",
                                                        "Image files (*.png *.jpeg *.jpg)")[0]

        if osPath.isfile(self.filePathName):
            fileName, fileExt = osPath.splitext(self.filePathName)

            if fileExt == '.jpg' or fileExt == '.jpeg' or fileExt == '.png':
                date = datetime.now()
                randomSuffix = "".join(random.choice(string.ascii_lowercase) for i in range(15))

                self.attachedFilePath = osPath.join("assets", "media", "people-media", "photos",
                                                     ("{:%d%b%Y_%Hh%Mm}".format(date) + randomSuffix + fileExt))
                self.attachedResizedFilePath = osPath.join("assets", "media", "people-media", "photos_resized",
                                                            ("{:%d%b%Y_%Hh%Mm}".format(date) + randomSuffix + "_resized" + fileExt))
                self.attachedThumbnailPath = osPath.join("assets", "media", "people-media", "photos_thumbnails",
                                                            ("{:%d%b%Y_%Hh%Mm}".format(date) + randomSuffix + "_resized.png"))


                QMessageBox.information(self, "Info", "File attached successfully")

            else:
                QMessageBox.information(self, "Info", "Wrong file type!")
        else:
            QMessageBox.information(self, "Info", "No file selected")

    ################ Image processing functions ##########################################
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
    def crop_max_square(self, pil_img):
        return self.crop_center(pil_img, min(pil_img.size), min(pil_img.size))

    # crop a square image into a circular image
    def mask_circle_transparent(self, pil_img, crop_width, crop_height, blur_radius, offset=0):
        img_width, img_height = pil_img.size
        pil_img.crop(((img_width - crop_width) // 2,
                      (img_height - crop_height) // 2,
                      (img_width + crop_width) // 2,
                      (img_height + crop_height) // 2))

        offset = blur_radius * 2 + offset
        mask = Image.new("L", pil_img.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((offset, offset, pil_img.size[0] - offset, pil_img.size[1] - offset), fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(blur_radius))

        result = pil_img.copy()
        result.putalpha(mask)

        return result


# class NewLineEdit(QLineEdit):
#
#     def __init__(self, label, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.label = label
#         self.lrect = self.fontMetrics().boundingRect(label)
#         self.setStyleSheet(f'''
#         QLineEdit {{
#             background-color: rgba(0, 0, 0, 0%);
#             border: none;
#             padding: 9px;
#             margin-top: {self.lrect.height() / 2}px;
#             color: blue;
#         }}''')
#         self.setAttribute(Qt.WA_MacShowFocusRect, False)
#         self.setMinimumWidth(200)
#
#     def paintEvent(self, event):
#         super().paintEvent(event)
#         w, h = self.width(), self.height()
#         lh = self.lrect.height() / 2
#
#         path = QPainterPath()
#         path.moveTo(30, lh + 3)
#         path.lineTo(9, lh + 3)
#         path.quadTo(3, lh + 3, 3, lh + 9)
#         path.lineTo(3, h - 9)
#         path.quadTo(3, h - 3, 9, h - 3)
#         path.lineTo(w - 9, h - 3)
#         path.quadTo(w - 3, h - 3, w - 3, h - 9)
#         path.lineTo(w - 3, lh + 9)
#         path.quadTo(w - 3, lh + 3, w - 9, lh + 3)
#         path.lineTo(42 + self.lrect.width(), lh + 3)
#
#         qp = QPainter(self)
#         qp.setRenderHint(QPainter.Antialiasing)
#         qp.setPen(QPen(QColor('#000000'), 1))
#         qp.drawPath(path)
#         qp.setPen(Qt.black)
#         qp.drawText(36, self.lrect.height(), self.label)
