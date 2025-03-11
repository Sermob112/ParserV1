# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'untitled.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
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
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow,
    QMenuBar, QProgressBar, QPushButton, QSizePolicy,
    QStatusBar, QTextBrowser, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(760, 657)
        font = QFont()
        font.setPointSize(14)
        MainWindow.setFont(font)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.Parse_but = QPushButton(self.centralwidget)
        self.Parse_but.setObjectName(u"Parse_but")
        self.Parse_but.setGeometry(QRect(20, 280, 171, 61))
        self.Parse_but.setStyleSheet(u"font: 14pt \"Impact\";")
        self.textBrowser = QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName(u"textBrowser")
        self.textBrowser.setGeometry(QRect(220, 290, 511, 311))
        self.textBrowser.setStyleSheet(u"font: 10pt \"Impact\";")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(220, 250, 151, 31))
        self.label.setStyleSheet(u"font: 14pt \"Impact\";")
        self.FilePathIn = QLineEdit(self.centralwidget)
        self.FilePathIn.setObjectName(u"FilePathIn")
        self.FilePathIn.setGeometry(QRect(150, 70, 581, 31))
        self.FilePathIn.setStyleSheet(u"font: 12pt \"Impact\";")
        self.InputFileBut = QPushButton(self.centralwidget)
        self.InputFileBut.setObjectName(u"InputFileBut")
        self.InputFileBut.setGeometry(QRect(20, 50, 121, 51))
        self.InputFileBut.setStyleSheet(u"font: 12pt \"Impact\";")
        self.OutPutFileBut = QPushButton(self.centralwidget)
        self.OutPutFileBut.setObjectName(u"OutPutFileBut")
        self.OutPutFileBut.setGeometry(QRect(20, 130, 121, 51))
        self.OutPutFileBut.setStyleSheet(u"font: 12pt \"Impact\";")
        self.FilePathOut = QLineEdit(self.centralwidget)
        self.FilePathOut.setObjectName(u"FilePathOut")
        self.FilePathOut.setGeometry(QRect(150, 150, 581, 31))
        self.FilePathOut.setStyleSheet(u"font: 12pt \"Impact\";")
        self.label_2 = QLabel(self.centralwidget)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(20, 10, 471, 21))
        self.label_2.setStyleSheet(u"font: 14pt \"Impact\";")
        self.Stop_but = QPushButton(self.centralwidget)
        self.Stop_but.setObjectName(u"Stop_but")
        self.Stop_but.setGeometry(QRect(20, 360, 171, 61))
        self.Stop_but.setStyleSheet(u"font: 14pt \"Impact\";")
        self.progressBar = QProgressBar(self.centralwidget)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setGeometry(QRect(20, 200, 711, 21))
        self.progressBar.setValue(24)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 760, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Parser 0.1b", None))
        self.Parse_but.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u0441\u0438\u0442\u044c", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u0416\u0443\u0440\u043d\u0430\u043b \u0441\u043e\u0431\u044b\u0442\u0438\u0439", None))
        self.FilePathIn.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 csv \u0444\u0430\u0439\u043b", None))
        self.FilePathIn.setPlaceholderText("")
        self.InputFileBut.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0440\u0430\u0442\u044c \u0444\u0430\u0439\u043b", None))
        self.OutPutFileBut.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0433\u0440\u0443\u0437\u0438\u0442\u044c \u0432", None))
        self.FilePathOut.setText(QCoreApplication.translate("MainWindow", u"\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u043c\u0435\u0441\u0442\u043e, \u043a\u0443\u0434\u0430 \u0431\u0443\u0434\u0443\u0442 \u0441\u043e\u0445\u0440\u0430\u043d\u0435\u043d\u044b \u0444\u0430\u0439\u043b\u044b", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0430\u0440\u0441\u0435\u0440 223-\u0424\u0417", None))
        self.Stop_but.setText(QCoreApplication.translate("MainWindow", u"\u041f\u0440\u0438\u043e\u0441\u0442\u0430\u043d\u043e\u0432\u0438\u0442\u044c", None))
    # retranslateUi

