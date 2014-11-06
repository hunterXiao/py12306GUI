#!/usr/bin/env python
#-*-coding:utf8-*-

import sys
import urllib

import stationSelect

from PyQt4 import QtCore, QtGui
from orderflow import getVerifyCode, init

try:
    _fromUTF8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUTF8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

#############################################################################################
class LoginForm(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUTF8("Form"))
        Form.setEnabled(True)
        Form.resize(360, 260)
        
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        
        Form.setSizePolicy(sizePolicy)
        Form.setMinimumSize(QtCore.QSize(360, 260))
        Form.setMaximumSize(QtCore.QSize(360, 260))
        
        font = QtGui.QFont()
        font.setFamily(_fromUTF8("Consolas"))
        font.setPointSize(12)
        
        Form.setFont(font)
        Form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Form.setAcceptDrops(False)
        
        self.user = QtGui.QLabel(Form)
        self.user.setGeometry(QtCore.QRect(40, 50, 61, 21))
        
        font = QtGui.QFont()
        #font.setFamily(_fromUTF8("Consolas"))
        font.setPointSize(12)
        
        self.user.setFont(font)
        self.user.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.user.setObjectName(_fromUTF8("user"))
        
        self.passwd = QtGui.QLabel(Form)
        self.passwd.setGeometry(QtCore.QRect(40, 110, 61, 16))
        
        font = QtGui.QFont()
        font.setFamily(_fromUTF8("Consolas"))
        font.setPointSize(12)
        self.passwd.setFont(font)
        self.passwd.setObjectName(_fromUTF8("passwd"))
        self.captcha = QtGui.QLabel(Form)
        self.captcha.setGeometry(QtCore.QRect(40, 160, 61, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUTF8("Consolas"))
        font.setPointSize(12)
        self.captcha.setFont(font)
        self.captcha.setObjectName(_fromUTF8("captcha"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 220, 78, 26))
        self.pushButton.setObjectName(_fromUTF8("pushButton"))
        self.userEdit = QtGui.QLineEdit(Form)
        self.userEdit.setGeometry(QtCore.QRect(110, 50, 140, 26))
        self.userEdit.setObjectName(_fromUTF8("userEdit"))
        self.passwdEdit = QtGui.QLineEdit(Form)
        self.passwdEdit.setGeometry(QtCore.QRect(110, 110, 140, 26))
        font = QtGui.QFont()
        font.setFamily(_fromUTF8("Consolas"))
        self.passwdEdit.setFont(font)
        self.passwdEdit.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.passwdEdit.setInputMask(_fromUTF8(""))
        self.passwdEdit.setMaxLength(50)
        self.passwdEdit.setFrame(True)
        self.passwdEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwdEdit.setObjectName(_fromUTF8("passwdEdit"))
        self.captchaEdit = QtGui.QLineEdit(Form)
        self.captchaEdit.setGeometry(QtCore.QRect(110, 160, 140, 26))
        self.captchaEdit.setObjectName(_fromUTF8("captchaEdit"))
        self.VerifyCode = ImageLabel(Form)
        self.VerifyCode.setGeometry(QtCore.QRect(270,160,78,26))
        self.VerifyCode.setObjectName(_fromUTF8("VerifyCode"))

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "登陆12306", None))
        self.user.setText(_translate("Form", "用户名：", None))
        self.passwd.setText(_translate("Form", "密   码：", None))
        self.captcha.setText(_translate("Form", "验证码：", None))
        self.pushButton.setText(_translate("Form", "登陆", None))

#自定义可点击的Label,重写mousePressEvent()方法实现Label的click()信号
class ImageLabel(QtGui.QLabel):
    """docstring for ImageLable"""
    clicked = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super(ImageLabel, self).__init__(parent)
        self.refreshImg(first = True)
        self.clicked.connect(self.refreshImg)

    def mousePressEvent(self,event):
        event.accept()
        self.clicked.emit()

    def refreshImg(self, first = False):
        retval = getVerifyCode(first)
        if retval:
            self.setPixmap(QtGui.QPixmap(_fromUTF8(retval)))
        else:
            QtGui.QMessageBox.critical(self,"Error",_fromUTF8(u"网络连接异常,验证码获取失败"))
            sys.exit()

class LoginFrame(QtGui.QDialog):
    """docstring for LoginFrame"""
    def __init__(self):
        super(LoginFrame, self).__init__()
        self.ui=LoginForm()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.check)

    def check(self):
        if self.ui.userEdit.text() == 'admin' and self.ui.passwdEdit.text() == 'passwd':
            self.accept()
        else:
            QtGui.QMessageBox.critical(self,u'登陆失败',u"用户名或密码错误！")


class MainWindow(QtGui.QDialog):
    seat = QtCore.QStringList()
    seat<<u"二等座"<<u"软卧"<<u"硬卧"<<u"硬座"<<u"无票"
    seatModel = QtGui.QStringListModel(seat)
    def __init__(self,parent=None):
        super(MainWindow,self).__init__(parent)

        fromLabel = QtGui.QLabel(_fromUTF8('出发地:'))
        toLabel = QtGui.QLabel(_fromUTF8('目的地:'))
        dateLabel = QtGui.QLabel(_fromUTF8('出发日期:'))
        trainLabel = QtGui.QLabel(_fromUTF8('车次:'))
        seatLabel = QtGui.QLabel(_fromUTF8('席别:'))
        pgrLabel = QtGui.QLabel(_fromUTF8('乘车人:'))

        self.fromEdit = PersonalLineEdit("fromEdit", self)
        self.toEdit = PersonalLineEdit("toEdit", self)
        self.fromEdit.clicked.connect(self.createStationSelect)
        self.toEdit.clicked.connect(self.createStationSelect)


        self.dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate())
        self.dateEdit.setCalendarPopup(True)

        self.trainEdit = PersonalLineEdit('trainEdit', self)

        self.seatComboBox = QtGui.QComboBox()
        self.seatComboBox.setModel(self.seatModel)

        self.pgrListView = QtGui.QListView()
        
        self.queryButton = QtGui.QPushButton(_fromUTF8('查询'))
        self.addButton = QtGui.QPushButton(_fromUTF8('添加'))
        self.delButton = QtGui.QPushButton(_fromUTF8('删除'))
        self.runButton = QtGui.QPushButton(_fromUTF8('开始'))

        layout = QtGui.QGridLayout()
        layout.addWidget(fromLabel,0,0)
        layout.addWidget(toLabel,1,0)
        layout.addWidget(dateLabel,2,0)
        layout.addWidget(trainLabel,3,0)
        layout.addWidget(seatLabel,4,0)
        layout.addWidget(pgrLabel,5,0)

        layout.addWidget(self.fromEdit,0,1)
        layout.addWidget(self.toEdit,1,1)
        layout.addWidget(self.dateEdit,2,1)
        layout.addWidget(self.trainEdit,3,1)
        layout.addWidget(self.seatComboBox,4,1)
        layout.addWidget(self.pgrListView,5,1,4,1)
        layout.addWidget(self.queryButton, 3, 2)
        layout.addWidget(self.addButton,7,2)
        layout.addWidget(self.delButton,8,2)
        layout.addWidget(self.runButton,9,1)

        self.setLayout(layout)
        self.setWindowTitle(_fromUTF8(u"12306订票助手"))

        self.window = None

    def createStationSelect(self,tag):
        self.window=stationSelect.Window(tag,self)
        self.window.exec_()


########################################################################
class PersonalLineEdit(QtGui.QLineEdit):
    """"""
    clicked = QtCore.pyqtSignal(str)
    #----------------------------------------------------------------------
    #tag 用于实例QLineEdit标签，以便于clicked信号携带，用于识别具体为哪个QLineEdit
    def __init__(self,tag,parent=None):
        """Constructor"""
        super(PersonalLineEdit, self).__init__(parent)
        self._tag = tag
    def mousePressEvent(self,event):
        event.accept()
        self.clicked.emit(self._tag)



def main():
    app=QtGui.QApplication(sys.argv)
    init() 
    login=LoginFrame()
    if login.exec_():
        mw=MainWindow()      
        mw.show()
        sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()
