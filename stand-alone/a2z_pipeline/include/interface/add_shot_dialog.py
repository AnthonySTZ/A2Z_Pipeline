# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'add_shot_dialog.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QDialog, QGridLayout,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(365, 132)
        self.horizontalLayout = QHBoxLayout(Dialog)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.le_shot_name = QLineEdit(self.widget)
        self.le_shot_name.setObjectName(u"le_shot_name")
        font = QFont()
        font.setPointSize(10)
        self.le_shot_name.setFont(font)

        self.gridLayout_2.addWidget(self.le_shot_name, 0, 1, 1, 1)

        self.sb_shot_number = QSpinBox(self.widget)
        self.sb_shot_number.setObjectName(u"sb_shot_number")
        self.sb_shot_number.setMaximumSize(QSize(16777215, 16777215))
        self.sb_shot_number.setFont(font)
        self.sb_shot_number.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.sb_shot_number.setMaximum(999)

        self.gridLayout_2.addWidget(self.sb_shot_number, 1, 1, 1, 1)

        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMaximumSize(QSize(16777215, 25))

        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMaximumSize(QSize(16777215, 40))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, -1, 0, -1)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.pb_ok = QPushButton(self.widget_2)
        self.pb_ok.setObjectName(u"pb_ok")

        self.horizontalLayout_2.addWidget(self.pb_ok)

        self.pb_cancel = QPushButton(self.widget_2)
        self.pb_cancel.setObjectName(u"pb_cancel")

        self.horizontalLayout_2.addWidget(self.pb_cancel)


        self.gridLayout_2.addWidget(self.widget_2, 2, 1, 1, 1)

        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)


        self.horizontalLayout.addWidget(self.widget)


        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.le_shot_name.setPlaceholderText(QCoreApplication.translate("Dialog", u"Enter shot name..", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Shot Number :", None))
        self.pb_ok.setText(QCoreApplication.translate("Dialog", u"Ok", None))
        self.pb_cancel.setText(QCoreApplication.translate("Dialog", u"Cancel", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Shot Name :", None))
    # retranslateUi

