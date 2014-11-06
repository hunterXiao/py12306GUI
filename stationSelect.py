#!/usr/bin/env python
#-*-coding:utf8-*-

import sys

from PyQt4 import QtCore, QtGui
from autostation import stationQuery, station_matched

try:
    _transUtf8 = QtCore.QString.fromUtf8
except:
    def _transUtf8(s):
        return s

#站点Model表头
#车站格式：bjb|北京北|VAP|beijingbei|bjb|0

code,stationName,stationCode,qp,jp = range(0,5)

########################################################################
class Window(QtGui.QDialog):
    """"""

    #----------------------------------------------------------------------
    def __init__(self,tag,parent=None):
        """Constructor"""

        super(Window, self).__init__(parent)

        #通过self.fatherWindow属性设置父窗体QLineEdit的text
        self.fatherWindow=parent
        self._tag = tag

        self.label = QtGui.QLabel(_transUtf8('站点名称(简拼):'))
        self.lineEdit = QtGui.QLineEdit()
        self.label.setBuddy(self.lineEdit)

        self.lineEdit.textChanged.connect(self.findData)

        self.sourceModel = QtGui.QStandardItemModel(0,5,self)
        self.proxymodel = QtGui.QSortFilterProxyModel()
        self.proxymodel.setSourceModel(self.sourceModel)
        self.proxymodel.sort(5)
        self.initModel()


        self.treeview  = QtGui.QTableView()
        self.treeview.setModel(self.proxymodel)
        self.treeview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeview.doubleClicked.connect(self.getWholeRowData)

        layout = QtGui.QGridLayout()
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.lineEdit,0,1)
        layout.addWidget(self.treeview,1,0,1,6)

        self.setLayout(layout)
        self.setWindowTitle(_transUtf8('站点查询'))
        self.resize(535,300)

    def initModel(self):
        self.sourceModel.setHeaderData(code,QtCore.Qt.Horizontal,_transUtf8(u"编码"))
        self.sourceModel.setHeaderData(stationName,QtCore.Qt.Horizontal,_transUtf8(u"车站名称"))
        self.sourceModel.setHeaderData(stationCode,QtCore.Qt.Horizontal,_transUtf8(u"车站代码"))
        self.sourceModel.setHeaderData(qp, QtCore.Qt.Horizontal, _transUtf8(u"全拼"))
        self.sourceModel.setHeaderData(jp,QtCore.Qt.Horizontal,_transUtf8(u"简拼"))
        # self.sourceModel.setHeaderData(order,QtCore.Qt.Horizontal,_transUtf8(u"排位"))


    def addItem(self,stationlist):
        if stationlist is not None:
            for data in stationlist:
                self.sourceModel.insertRow(0)
                for column in xrange(5):
                    if column == 0:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.abbr))
                    elif column == 1:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.name))
                    elif column == 2:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.telecode))
                    elif column == 3:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.pinyin))
                    elif column == 4:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.pyabbr))
                    # elif column == 5:
                    #     self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.f))
        else:
            self.sourceModel.removeRows(0,self.sourceModel.rowCount())

    def findData(self): 
        query= self.lineEdit.text()
        stationQuery(str(query))
        self.sourceModel.removeRows(0,self.sourceModel.rowCount())
        self.addItem(station_matched)

    def getWholeRowData(self,index):
        m = index.model()
        t = m.index(index.row(),1)
        data = t.data().toString()
        if self._tag == "fromEdit":
            self.fatherWindow.fromEdit.setText(data)
            self.close()
        elif self._tag == "toEdit":
            self.fatherWindow.toEdit.setText(data)
            self.close()
        #for columnIndex in xrange(m.columnCount()):
            #x = m.index(index.row(),columnIndex)
            #data = x.data().toString()
            #QtGui.QMessageBox.information(self, "Information", data)
