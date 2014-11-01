#-*-coding:utf8-*-

from PyQt4 import QtCore, QtGui
from autostation import stationQuery
import sys
#import login
try:
    _transUtf8 = QtCore.QString.fromUtf8
except:
    def _transUtf8(s):
        return s
    
#站点Model表头
#车站格式：bjb|北京北|VAP|beijingbei|bjb|0

code,stationName,stationCode,qp,jp,order = range(0,6)

##def createStationModel(stationList,parent):
##    model = QtGui.QStandardItemModel(0,6,parent)
##    
##    model.setHeaderData(code,QtCore.Qt.Horizontal,"Code")
##    model.setHeaderData(stationName,QtCore.Qt.Horizontal,"StationName")
##    model.setHeaderData(stationCode,QtCore.Qt.Horizontal,"StationCode")
##    model.setHeaderData(qp,QtCore.Qt.Horizontal,"StationQP")
##    model.setHeaderData(jp,QtCore.Qt.Horizontal,"StationJP")
##    model.setHeaderData(order,QtCore.Qt.Horizontal,"Order")
##    
##    for data in stationList:
##        model.insertRow(0)
##        for column in xrange(6):
##            if column == 0:
##                model.setData(model.index(0, column), _transUtf8(data.a))
##            elif column == 1:
##                model.setData(model.index(0, column), _transUtf8(data.b))
##            elif column == 2:
##                model.setData(model.index(0, column), _transUtf8(data.c))
##            elif column == 3:
##                model.setData(model.index(0, column), _transUtf8(data.d))
##            elif column == 4:
##                model.setData(model.index(0, column), _transUtf8(data.e))
##            elif column == 5:
##                model.setData(model.index(0, column), _transUtf8(data.f))
##            
##    return model
    
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
        
        self.sourceModel = QtGui.QStandardItemModel(0,6,self)
        self.proxymodel = QtGui.QSortFilterProxyModel()
        self.proxymodel.setSourceModel(self.sourceModel)
        self.proxymodel.sort(5)
        self.initModel()
        
        
        self.treeview  = QtGui.QTableView()
##        self.treeview.setModel(self.sourceModel)
        self.treeview.setModel(self.proxymodel)
##        self.treeview.sortByColumn(5)
        self.treeview.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.treeview.doubleClicked.connect(self.getWholeRowData)
                
        layout = QtGui.QGridLayout()
        layout.addWidget(self.label,0,0)
        layout.addWidget(self.lineEdit,0,1)
        layout.addWidget(self.treeview,1,0,1,6)
        
        self.setLayout(layout)
        self.setWindowTitle(_transUtf8('站点查询'))
        self.resize(650,300)
        
    def initModel(self):
        self.sourceModel.setHeaderData(code,QtCore.Qt.Horizontal,_transUtf8(u"拼音编码"))
        self.sourceModel.setHeaderData(stationName,QtCore.Qt.Horizontal,_transUtf8(u"车站名称"))
        self.sourceModel.setHeaderData(stationCode,QtCore.Qt.Horizontal,_transUtf8(u"车站代码"))
        self.sourceModel.setHeaderData(qp, QtCore.Qt.Horizontal, _transUtf8(u"全拼"))
        self.sourceModel.setHeaderData(jp,QtCore.Qt.Horizontal,_transUtf8(u"简拼"))
        self.sourceModel.setHeaderData(order,QtCore.Qt.Horizontal,_transUtf8(u"排位"))
        
    
    def addItem(self,stationlist):
        if stationlist is not None:
            for data in stationlist:
                self.sourceModel.insertRow(0)
                for column in xrange(6):
                    if column == 0:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.a))
                    elif column == 1:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.b))
                    elif column == 2:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.c))
                    elif column == 3:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.d))
                    elif column == 4:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.e))
                    elif column == 5:
                        self.sourceModel.setData(self.sourceModel.index(0, column), _transUtf8(data.f))
        else:
            self.sourceModel.removeRows(0,self.sourceModel.columnCount())
    
    def findData(self,text):
        query=self.lineEdit.text()
        stationlist=stationQuery(str(query))
        B=self.sourceModel.removeRows(0,self.sourceModel.rowCount())
        self.addItem(stationlist)
        
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

if __name__=='__main__':
    app=QtGui.QApplication(sys.argv)
    window=Window()
    window.show()
    sys.exit(app.exec_())
    