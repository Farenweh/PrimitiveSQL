from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_load(object):
    def setupUi(self, load):
        load.setObjectName("load")
        load.resize(517, 244)
        self.centralwidget = QtWidgets.QWidget(load)
        self.centralwidget.setObjectName("centralwidget")
        self.load_label = QtWidgets.QLabel(self.centralwidget)
        self.load_label.setGeometry(QtCore.QRect(20, 70, 131, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(11)
        self.load_label.setFont(font)
        self.load_label.setTextFormat(QtCore.Qt.AutoText)
        self.load_label.setObjectName("load_label")
        self.queding_button = QtWidgets.QPushButton(self.centralwidget)
        self.queding_button.setGeometry(QtCore.QRect(110, 140, 91, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(11)
        self.queding_button.setFont(font)
        self.queding_button.setStyleSheet("border-ridius:10px;")
        self.queding_button.setObjectName("queding_button")
        self.tuichu_button = QtWidgets.QPushButton(self.centralwidget)
        self.tuichu_button.setGeometry(QtCore.QRect(310, 140, 91, 41))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(11)
        self.tuichu_button.setFont(font)
        self.tuichu_button.setObjectName("tuichu_button")
        self.load_input = QtWidgets.QLineEdit(self.centralwidget)
        self.load_input.setGeometry(QtCore.QRect(160, 80, 321, 31))
        self.load_input.setObjectName("lineEdit")
        load.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(load)
        self.statusbar.setObjectName("statusbar")
        load.setStatusBar(self.statusbar)

        self.retranslateUi(load)
        QtCore.QMetaObject.connectSlotsByName(load)

    def retranslateUi(self, load):
        _translate = QtCore.QCoreApplication.translate
        load.setWindowTitle(_translate("load", "MainWindow"))
        self.load_label.setText(_translate("load", "挂载数据库地址"))
        self.queding_button.setText(_translate("load", "确定"))
        self.tuichu_button.setText(_translate("load", "退出"))


class Ui_warning(object):
    def setupUi(self, warning):
        warning.setObjectName("warning")
        warning.resize(393, 184)
        self.warnnig_wid = QtWidgets.QWidget(warning)
        self.warnnig_wid.setObjectName("warnnig_wid")
        self.warning_lable = QtWidgets.QLabel(self.warnnig_wid)
        self.warning_lable.setGeometry(QtCore.QRect(90, 20, 281, 121))
        self.warning_lable.setMaximumSize(QtCore.QSize(281, 121))
        font = QtGui.QFont()
        font.setFamily("楷体")
        font.setPointSize(14)
        self.warning_lable.setFont(font)
        self.warning_lable.setObjectName("warning_lable")
        warning.setCentralWidget(self.warnnig_wid)
        self.statusbar = QtWidgets.QStatusBar(warning)
        self.statusbar.setObjectName("statusbar")
        warning.setStatusBar(self.statusbar)

        self.retranslateUi(warning)
        QtCore.QMetaObject.connectSlotsByName(warning)

    def retranslateUi(self, warning):
        _translate = QtCore.QCoreApplication.translate
        warning.setWindowTitle(_translate("warning", "MainWindow"))
        self.warning_lable.setText(_translate("warning", "一条提示语句....."))


class Ui_dbdatabase(object):
    def setupUi(self, dbdatabase):
        dbdatabase.setObjectName("dbdatabase")
        dbdatabase.resize(889, 752)
        self.centralwidget = QtWidgets.QWidget(dbdatabase)
        self.centralwidget.setObjectName("centralwidget")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setGeometry(QtCore.QRect(0, 0, 891, 731))
        self.widget.setAutoFillBackground(False)
        self.widget.setStyleSheet("background-color: rgb(239, 239, 239);\n"
                                  "border-radius:10px;")
        self.widget.setObjectName("widget")
        self.file_view_frame = QtWidgets.QFrame(self.widget)
        self.file_view_frame.setGeometry(QtCore.QRect(10, 10, 211, 711))
        self.file_view_frame.setStyleSheet("background-color: rgb(197, 197, 197);")
        self.file_view_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.file_view_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.file_view_frame.setObjectName("file_view_frame")
        self.file_view_tag_label = QtWidgets.QLabel(self.file_view_frame)
        self.file_view_tag_label.setGeometry(QtCore.QRect(10, 10, 101, 16))
        self.file_view_tag_label.setStyleSheet("font: 11pt \"楷体\";")
        self.file_view_tag_label.setObjectName("file_view_tag_label")
        self.file_list_browser = QtWidgets.QTextBrowser(self.file_view_frame)
        self.file_list_browser.setGeometry(QtCore.QRect(10, 30, 191, 671))
        self.file_list_browser.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.file_list_browser.setObjectName("file_list_browser")
        self.delete_button = QtWidgets.QPushButton(self.file_view_frame)
        self.delete_button.setGeometry(QtCore.QRect(20, 660, 81, 31))
        self.delete_button.setStyleSheet("font: 11pt \"楷体\";\n"
                                         "border-style: solid;\n"
                                         "background-color: rgb(255, 255, 255);\n"
                                         "border-width: 1px;\n"
                                         "border-color:rgb(81, 81, 81);\n"
                                         "border-riduis:none;")
        self.delete_button.setObjectName("delete_button")
        self.refresh_button = QtWidgets.QPushButton(self.file_view_frame)
        self.refresh_button.setGeometry(QtCore.QRect(110, 660, 81, 31))
        self.refresh_button.setStyleSheet("font: 11pt \"楷体\";\n"
                                          "border-style: solid;\n"
                                          "background-color: rgb(255, 255, 255);\n"
                                          "border-width: 1px;\n"
                                          "border-color:rgb(81, 81, 81);\n"
                                          "border-riduis:none;")
        self.refresh_button.setObjectName("refresh_button")
        self.result_view_frame = QtWidgets.QFrame(self.widget)
        self.result_view_frame.setGeometry(QtCore.QRect(230, 300, 651, 421))
        self.result_view_frame.setStyleSheet("background-color: rgb(193, 193, 193);")
        self.result_view_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.result_view_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.result_view_frame.setObjectName("result_view_frame")
        self.result_tag_label = QtWidgets.QLabel(self.result_view_frame)
        self.result_tag_label.setGeometry(QtCore.QRect(10, 10, 81, 16))
        self.result_tag_label.setStyleSheet("font: 11pt \"楷体\";")
        self.result_tag_label.setObjectName("result_tag_label")
        self.result_browser = QtWidgets.QTextBrowser(self.result_view_frame)
        self.result_browser.setGeometry(QtCore.QRect(10, 30, 631, 381))
        self.result_browser.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                          "border-radius:5px;\n"
                                          "font: 11pt \"楷体\";\n"
                                          "font-color:rgb(176, 176, 176);")
        self.result_browser.setObjectName("result_browser")
        self.sql_input_frame = QtWidgets.QFrame(self.widget)
        self.sql_input_frame.setGeometry(QtCore.QRect(230, 10, 651, 281))
        self.sql_input_frame.setStyleSheet("background-color: rgb(193, 193, 193);")
        self.sql_input_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.sql_input_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.sql_input_frame.setObjectName("sql_input_frame")
        self.sqlinput_tag_label = QtWidgets.QLabel(self.sql_input_frame)
        self.sqlinput_tag_label.setGeometry(QtCore.QRect(20, 10, 72, 15))
        self.sqlinput_tag_label.setStyleSheet("font: 11pt \"楷体\";")
        self.sqlinput_tag_label.setObjectName("sqlinput_tag_label")
        self.sql_input_button = QtWidgets.QPushButton(self.sql_input_frame)
        self.sql_input_button.setGeometry(QtCore.QRect(540, 230, 91, 31))
        self.sql_input_button.setStyleSheet("font: 11pt \"楷体\";\n"
                                            "border-style: solid;\n"
                                            "background-color: rgb(255, 255, 255);\n"
                                            "border-width: 1px;\n"
                                            "border-color:rgb(81, 81, 81);\n"
                                            "border-riduis:none;")
        self.sql_input_button.setObjectName("sql_input_button")
        self.sql_input_widget = QtWidgets.QTextEdit(self.sql_input_frame)
        self.sql_input_widget.setGeometry(QtCore.QRect(10, 30, 631, 241))
        self.sql_input_widget.setStyleSheet("background-color: rgb(255, 255, 255);\n"
                                            "border-radius:5px;\n"
                                            "font: 11pt \"楷体\";\n"
                                            "font-color:rgb(176, 176, 176);")
        self.sql_input_widget.setObjectName("sql_input_widget")
        self.sqlinput_tag_label.raise_()
        self.sql_input_widget.raise_()
        self.sql_input_button.raise_()
        dbdatabase.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(dbdatabase)
        self.statusbar.setObjectName("statusbar")
        dbdatabase.setStatusBar(self.statusbar)

        self.retranslateUi(dbdatabase)
        QtCore.QMetaObject.connectSlotsByName(dbdatabase)

    def retranslateUi(self, dbdatabase):
        _translate = QtCore.QCoreApplication.translate
        dbdatabase.setWindowTitle(_translate("dbdatabase", "MainWindow"))
        self.file_view_tag_label.setText(_translate("dbdatabase", "数据库导航"))
        self.delete_button.setText(_translate("dbdatabase", "删除"))
        self.refresh_button.setText(_translate("dbdatabase", "更新"))
        self.result_tag_label.setText(_translate("dbdatabase", "操作结果"))
        self.sqlinput_tag_label.setText(_translate("dbdatabase", "SQL语句"))
        self.sql_input_button.setText(_translate("dbdatabase", "确定"))
        self.sql_input_widget.setAccessibleName(
            _translate("dbdatabase", "<html><head/><body><p>Enter</p></body></html>"))
        self.sql_input_widget.setHtml(_translate("dbdatabase",
                                                 "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
                                                 "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
                                                 "p, li { white-space: pre-wrap; }\n"
                                                 "</style></head><body style=\" font-family:\'楷体\'; font-size:11pt; font-weight:400; font-style:normal;\">\n"
                                                 "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">请输入SQL语句</p></body></html>"))
