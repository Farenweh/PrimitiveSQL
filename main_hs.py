from __future__ import print_function
from __future__ import division
from PyQt5.QtWidgets import QMessageBox,QApplication
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QEventLoop, QTimer
import gui_win
import inter_func
import db_func
import cfg

class EmittingStr(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str) #定义一个发送str的信号
    def write(self, text):
      self.textWritten.emit(str(text))

class Win_work(gui_win.Ui_dbdatabase,QtWidgets.QMainWindow):

    def __init__(self):
        super(Win_work, self).__init__()
        self.setupUi(self)

        #控制台内容定位到textBowser中
        sys.stdout = EmittingStr(textWritten=self.outputWritten)
        sys.stderr = EmittingStr(textWritten=self.outputWritten)

        # 显示查询结果
        # 显示数据库数据列表
        # 绑定输入sql语句后的确定按钮
        self.sql_input_button.clicked.connect(self.get_sql)
        self.delete_button.clicked.connect(self.delete_db)
        self.refresh_button.clicked.connect(self.refresh_db)

    def outputWritten(self, text):
        cursor = self.result_browser.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.result_browser.setTextCursor(cursor)
        self.result_browser.ensureCursorVisible()

    def get_sql(self):
        sql = self.sql_input_widget.toPlainText()
        inter_func.inited(sql)

    #待调试
    def delete_db(self):
        choose = QMessageBox.information(self, "提醒", "是否需要移除当前数据库", QMessageBox.Yes|QMessageBox.No)
        if choose == QMessageBox.Yes:
            if inter_func.delete_database():
                QMessageBox.information(self, "提醒", "%s已经移除" % db_func.active_database)
                #child_win.show()
                self.close()
            else:
                self.file_list_browser.append("database是空")

    def file_view(self):
        if len(cfg.active_database.resource) == 0:
            #问题在这里！
            self.file_list_browser.append("暂无数据")
        else:
            for i in range(len(cfg.active_database.resource)):
                self.file_list_browser.append("table: " + cfg.active_database.resource[i].name)
                for j in cfg.active_database.resource[i].column:
                    self.file_list_browser.append('    ' + j)

    def refresh_db(self):
        inter_func.refresh()
        self.file_list_browser.clear()
        self.file_view()



class Win_load(gui_win.Ui_load, QtWidgets.QMainWindow):
    def __init__(self):
        super(Win_load, self).__init__()
        self.setupUi(self)
        self.queding_button.clicked.connect(self.get_db_name)
        self.tuichu_button.clicked.connect(self.close)

    def get_db_name(self):
        db_name = self.load_input.text()
        if inter_func.choose_database(db_name):
            warning = "%s已经打开"%db_name
            choose = QMessageBox.information(self, "提醒", warning, QMessageBox.Yes|QMessageBox.No, QMessageBox.Yes)
            if choose == QMessageBox.Yes:
                window_work.show()
                window_work.file_view()
                self.close()
        else:
            warning = "%s.db不存在\n是否需要创建该名数据库"%db_name
            choose = QMessageBox.information(self, "提醒", warning, QMessageBox.Yes | QMessageBox.No)
            if choose == QMessageBox.Yes:
                #创建一个新数据库
                if inter_func.create_database(db_name):
                    window_work.show()
                    window_work.file_view()
                    self.close()
                    QMessageBox.information(self, "提醒", "%s已创建" % db_name)
                else:
                    QMessageBox.information(self, "提醒", "已存在同名数据库")
            if choose == QMessageBox.No:
                pass


if __name__ == '__main__':
    inter_func.init()
    app_work = QtWidgets.QApplication(sys.argv)
    child_win = Win_load()
    window_work = Win_work()
    child_win.show()
    sys.exit(app_work.exec_())

    # inter_func.create_database('')
    # inter_func.choose_database('debug1')
    # print(cfg.active_database.name)
    # print('create table debug(col1 int)')
