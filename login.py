# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created: Sat Sep 13 13:32:24 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys,urllib2,urllib
from mainwindow import MainWindow
#import mainwindow
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)





class LoginForm(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
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
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(12)
        Form.setFont(font)
        Form.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Form.setAcceptDrops(False)
        self.user = QtGui.QLabel(Form)
        self.user.setGeometry(QtCore.QRect(40, 50, 61, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(12)
        self.user.setFont(font)
        self.user.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.user.setObjectName(_fromUtf8("user"))
        self.passwd = QtGui.QLabel(Form)
        self.passwd.setGeometry(QtCore.QRect(40, 110, 61, 16))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(12)
        self.passwd.setFont(font)
        self.passwd.setObjectName(_fromUtf8("passwd"))
        self.captcha = QtGui.QLabel(Form)
        self.captcha.setGeometry(QtCore.QRect(40, 160, 61, 21))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        font.setPointSize(12)
        self.captcha.setFont(font)
        self.captcha.setObjectName(_fromUtf8("captcha"))
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 220, 78, 26))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.userEdit = QtGui.QLineEdit(Form)
        self.userEdit.setGeometry(QtCore.QRect(110, 50, 140, 26))
        self.userEdit.setObjectName(_fromUtf8("userEdit"))
        self.passwdEdit = QtGui.QLineEdit(Form)
        self.passwdEdit.setGeometry(QtCore.QRect(110, 110, 140, 26))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Consolas"))
        self.passwdEdit.setFont(font)
        self.passwdEdit.setContextMenuPolicy(QtCore.Qt.PreventContextMenu)
        self.passwdEdit.setInputMask(_fromUtf8(""))
        self.passwdEdit.setMaxLength(50)
        self.passwdEdit.setFrame(True)
        self.passwdEdit.setEchoMode(QtGui.QLineEdit.Password)
        self.passwdEdit.setObjectName(_fromUtf8("passwdEdit"))
        self.captchaEdit = QtGui.QLineEdit(Form)
        self.captchaEdit.setGeometry(QtCore.QRect(110, 160, 140, 26))
        self.captchaEdit.setObjectName(_fromUtf8("captchaEdit"))
        self.VerifyCode = ImageLabel(Form)
        self.VerifyCode.setGeometry(QtCore.QRect(270,160,78,26))
        self.VerifyCode.setObjectName(_fromUtf8("VerifyCode"))

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
        self.refreshImg()
        self.clicked.connect(self.refreshImg)

    def mousePressEvent(self,event):
        event.accept()
        self.clicked.emit()

    def refreshImg(self):
        try:
            urllib.urlretrieve(r'https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand','getPassCodeNew.png')
            self.setPixmap(QtGui.QPixmap(_fromUtf8("getPassCodeNew.png")))
        except:
            QtGui.QMessageBox.critical(self,"Error",_fromUtf8(u"网络连接异常，程式关闭！"))
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


def main():
    app=QtGui.QApplication(sys.argv)
    login=LoginFrame()
    #login.show()
    if login.exec_():
        mw=MainWindow()      
        mw.show()
        sys.exit(app.exec_()) 


if __name__ == '__main__':
    main()

        
