#-*-coding:utf8-*-

__author__='hunterXiao'

from PyQt4 import QtCore,QtGui
import sys
import stationSelect

try:
	_fromUTF8 = QtCore.QString.fromUtf8
except:
	def _fromUTF8(s):
		return s

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

		self.fromEdit = PersonalLineEdit("fromEdit")
		self.toEdit = PersonalLineEdit("toEdit")
		self.fromEdit.clicked.connect(self.createStationSelect)
		self.toEdit.clicked.connect(self.createStationSelect)
		

		self.dateEdit = QtGui.QDateEdit(QtCore.QDate.currentDate())
		self.dateEdit.setCalendarPopup(True)

		self.trainEdit = QtGui.QLineEdit()

		self.seatComboBox = QtGui.QComboBox()
		self.seatComboBox.setModel(self.seatModel)

		self.pgrListView = QtGui.QListView()

		self.addButton = QtGui.QPushButton(u'添加')
		self.delButton = QtGui.QPushButton(u'删除')
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
		layout.addWidget(self.addButton,7,2)
		layout.addWidget(self.delButton,8,2)
		layout.addWidget(self.runButton,9,1)

		self.setLayout(layout)
		self.setWindowTitle(_fromUTF8(u"12306订票助手"))
		
		self.window = None
		
	def createStationSelect(self,tag):
		self.window=stationSelect.Window(tag,self)
		#self.window.show()
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

if __name__ == "__main__":
        app = QtGui.QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
