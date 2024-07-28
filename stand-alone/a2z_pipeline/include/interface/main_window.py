# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_window.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QGridLayout,
    QHeaderView, QLabel, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QTableWidget, QTableWidgetItem,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout_3 = QGridLayout(self.centralwidget)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        self.gridLayout_2 = QGridLayout(self.widget)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")
        font = QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)

        self.cb_projects = QComboBox(self.widget)
        self.cb_projects.setObjectName(u"cb_projects")
        self.cb_projects.setMinimumSize(QSize(150, 25))
        self.cb_projects.setMaximumSize(QSize(150, 25))

        self.gridLayout_2.addWidget(self.cb_projects, 0, 1, 1, 1)

        self.pb_add_projects = QPushButton(self.widget)
        self.pb_add_projects.setObjectName(u"pb_add_projects")
        self.pb_add_projects.setMinimumSize(QSize(25, 25))
        self.pb_add_projects.setMaximumSize(QSize(25, 25))

        self.gridLayout_2.addWidget(self.pb_add_projects, 0, 2, 1, 1)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout_2.addItem(self.horizontalSpacer, 0, 3, 1, 1)


        self.gridLayout_3.addWidget(self.widget, 0, 0, 1, 1)

        self.widget_2 = QWidget(self.centralwidget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.pb_add_shot = QPushButton(self.widget_2)
        self.pb_add_shot.setObjectName(u"pb_add_shot")

        self.gridLayout.addWidget(self.pb_add_shot, 0, 0, 1, 1)

        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.gridLayout.addItem(self.horizontalSpacer_2, 0, 1, 1, 1)

        self.tw_shots = QTableWidget(self.widget_2)
        if (self.tw_shots.columnCount() < 9):
            self.tw_shots.setColumnCount(9)
        __qtablewidgetitem = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(5, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(6, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(7, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.tw_shots.setHorizontalHeaderItem(8, __qtablewidgetitem8)
        self.tw_shots.setObjectName(u"tw_shots")
        self.tw_shots.setSelectionMode(QAbstractItemView.NoSelection)
        self.tw_shots.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.tw_shots.setHorizontalScrollMode(QAbstractItemView.ScrollPerItem)
        self.tw_shots.setSortingEnabled(False)
        self.tw_shots.horizontalHeader().setDefaultSectionSize(60)
        self.tw_shots.horizontalHeader().setStretchLastSection(True)
        self.tw_shots.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tw_shots, 1, 0, 1, 2)


        self.gridLayout_3.addWidget(self.widget_2, 1, 0, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Project :", None))
        self.pb_add_projects.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.pb_add_shot.setText(QCoreApplication.translate("MainWindow", u"Add Shot", None))
        ___qtablewidgetitem = self.tw_shots.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Shots", None));
        ___qtablewidgetitem1 = self.tw_shots.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"Name", None));
        ___qtablewidgetitem2 = self.tw_shots.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"Thumbnails", None));
        ___qtablewidgetitem3 = self.tw_shots.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"preprod", None));
        ___qtablewidgetitem4 = self.tw_shots.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"asset", None));
        ___qtablewidgetitem5 = self.tw_shots.horizontalHeaderItem(5)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"fx", None));
        ___qtablewidgetitem6 = self.tw_shots.horizontalHeaderItem(6)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"lighting", None));
        ___qtablewidgetitem7 = self.tw_shots.horizontalHeaderItem(7)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"comp", None));
        ___qtablewidgetitem8 = self.tw_shots.horizontalHeaderItem(8)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"Description", None));
    # retranslateUi

