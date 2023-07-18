from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtCore import *

import pandas as pd
import time

class TableEditorModel(QStandardItemModel):
    def __init__(self, defaultRowDict={}, row_direction="vertical", parent=None):
        super().__init__(parent)
        self.row_direction = row_direction
        self.checkedIndex = []
        self.defaultRowDict = defaultRowDict
        #self.appendDict(defaultRowDict)
        self.rowsRemoved.connect(self.dataChanged.emit)

    def appendDict(self,dictRow):
        df = self.exportDataFrame()
        df = pd.concat([df,pd.DataFrame([dictRow.values()], columns=dictRow.keys())],ignore_index=True).fillna("")
        self.importDataFrame(df)

    def appendListRow(self,listRow):
        textItemList = []
        for item in listRow:
            textItem = QStandardItem()
            if type(item)==str:
                textItem.setText(item)
            elif int(item) == int(str(int(item))):
                textItem.setText(str(item))
            else:
                textItem.setText(f'{item:.3f}')
            textItemList.append(textItem)
        if self.row_direction == "vertical":
            self.insertRow(self.rowCount(), textItemList)
        elif self.row_direction =="horizontal":
            self.insertColumn(self.columnCount(), textItemList)

    def paste_dataFrame(self,df_paste,row_start,col_start):
        if self.row_direction == "horizontal":
            df_paste = df_paste.T

        row_end = row_start + df_paste.shape[0]
        col_end = col_start + df_paste.shape[1]
        df_old = self.exportDataFrame()
                
        index = list(df_old.index)
        columns = list(df_old.columns)
        if row_end >= df_old.shape[0]:
            for i in range(df_old.shape[0],row_end):
                index.append(i)
        if col_end >= df_old.shape[1]:
            for i in range(df_old.shape[1],col_end):
                columns.append(i)
        df_new = pd.DataFrame(df_old, index=index,columns=columns)
        for i in range(row_start,row_end):
            for j in range(col_start,col_end):
                df_new.iloc[i,j] = df_paste.iloc[i-row_start,j-col_start]
        df_new.fillna("",inplace=True)
        self.importDataFrame(df_new)

    def importDataFrame(self,df):
        self.clear()
        self.checkedIndex = []
        if self.row_direction == "vertical":
            self.setHorizontalHeaderLabels(df.columns)
        elif self.row_direction =="horizontal":
            self.setVerticalHeaderLabels(df.columns)
        for i in range(df.shape[0]):
            self.appendListRow(df.iloc[i,:])
        if self.row_direction == "vertical":            
            self.setVerticalHeaderLabels([str(i) for i in df.index])
        elif self.row_direction =="horizontal":
            self.setHorizontalHeaderLabels([str(i) for i in df.index])
        self.dataChanged.emit(QModelIndex(),QModelIndex())

    def importMatrix(self,mat):
        self.clear()
        self.checkedIndex = []
        for i in range(mat.shape[0]):
            self.appendListRow(mat[i,:])

    def exportDataFrame(self):
        if self.row_direction == "vertical":
            columns = [self.horizontalHeaderItem(i).text() for i in range(self.columnCount())]
        elif self.row_direction =="horizontal":
            columns = [self.verticalHeaderItem(i).text() for i in range(self.rowCount())]
        return pd.DataFrame(self.exportList2D(), columns=columns)

    def exportList2D(self):
        list2D = []
        if self.row_direction == "vertical":
            for row in range(self.rowCount()):
                list2D.append([])
                for col in range(self.columnCount()):
                    text = self.item(row,col).text()
                    done = False
                    try:                        
                        if int(text) == int(str(int(text))):
                            list2D[row].append(int(text))
                            done = True
                    except ValueError:
                        pass
                    if done == False:
                        try:
                            list2D[row].append(float(text))
                        except ValueError:
                            list2D[row].append(text)
        elif self.row_direction == "horizontal":
            for col in range(self.columnCount()):
                list2D.append([])
                for row in range(self.rowCount()):
                    text = self.item(row,col).text()
                    done = False
                    try:                        
                        if int(text) == int(str(int(text))):
                            list2D[col].append(int(text))
                            done = True
                    except ValueError:
                        pass
                    if done == False:
                        try:
                            list2D[col].append(float(text))
                        except ValueError:
                            list2D[col].append(text)
        return list2D

class TableView(QTableView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFocusPolicy(Qt.StrongFocus)
        self.resizeColumnsToContents()
        self.setAcceptDrops(True)
        self.actions = {}

    def setModel(self,*args):
        super().setModel(*args)
        self.model().dataChanged.connect(self.resizeRowsToContents)
        self.model().dataChanged.connect(self.resizeColumnsToContents)
        self.resizeRowsToContents()
        self.resizeColumnsToContents()
        
    def selectAll(self):
        self.model().checkedIndex = [self.model().item(row, col).index() for col in range(self.model().columnCount()) for row in range(self.model().rowCount())]
        for itemIndex in self.model().checkedIndex:
            self.model().itemFromIndex(itemIndex).setBackground(QColor(125,125,125))

    def dragEnterEvent(self, e):
        e.accept()

    def dragMoveEvent(self, e):
        e.accept()

    def dropEvent(self, e):    
        e.accept()

    def contextMenuEvent(self, event):        
        menu = QMenu(self)
        self.actions["addUnit"] = QAction("Add Unit",self)
        self.actions["addUnit"].triggered.connect(self.addUnit)
        menu.addAction(self.actions["addUnit"])
        menu.exec(event.globalPos())

    def addUnit(self):
        self.model().appendDict(self.model().defaultRowDict)
        self.resizeColumnsToContents()

    def mousePressEvent(self,e):
        super().mousePressEvent(e)
        if e.button()==Qt.RightButton:
            for itemIndex in self.selectedIndexes():
                if itemIndex in self.model().checkedIndex:
                    self.model().checkedIndex.remove(itemIndex)
                    self.model().itemFromIndex(itemIndex).setBackground(QColor(255,255,255))
                else:
                    self.model().checkedIndex.append(itemIndex)
                    self.model().itemFromIndex(itemIndex).setBackground(QColor(125,125,125))

    def getChecked(self):
        return [[itemIndex.row(), itemIndex.column()] for itemIndex in self.model().checkedIndex]

    
    def keyPressEvent(self,event):
        if event.modifiers()==(Qt.ControlModifier):
            if event.key() == Qt.Key_C:
                self.c_copyContent()
            elif event.key() == Qt.Key_V:
                self.c_pasteContent()
        else:
            if event.key()==Qt.Key_Delete:       
                if self.model().row_direction == "vertical":
                    currentRows = []
                    for itemIndex in self.selectedIndexes():
                        row = itemIndex.row()
                        if row not in currentRows:
                            currentRows.append(row)
                    self.model().removeRows(currentRows[0],len(currentRows))
                elif self.model().row_direction == "horizontal":
                    currentColumns = []
                    for itemIndex in self.selectedIndexes():
                        column = itemIndex.column()
                        if column not in currentColumns:
                            currentColumns.append(column)
                    self.model().removeColumns(currentColumns[0],len(currentColumns))
                self.model().dataChanged.emit(QModelIndex(),QModelIndex())
            elif event.key()==Qt.Key_Insert:
                self.addUnit()

            numberMap = {Qt.Key_0:0,Qt.Key_1:1,Qt.Key_2:2,Qt.Key_3:3,Qt.Key_4:4,
                         Qt.Key_5:5,Qt.Key_6:6,Qt.Key_7:7,Qt.Key_8:8,Qt.Key_9:9,
                         Qt.Key_Plus:"+",Qt.Key_Minus:"-",Qt.Key_Period:'.',}
            charMap = {Qt.Key_A:"a",Qt.Key_B:"b",Qt.Key_C:"c",Qt.Key_D:"d",Qt.Key_E:"e",
                       Qt.Key_F:"f",Qt.Key_G:"g",Qt.Key_H:"h",Qt.Key_I:"i",Qt.Key_J:"j",
                       Qt.Key_K:"k",Qt.Key_L:"l",Qt.Key_M:"m",Qt.Key_N:"n",Qt.Key_O:"o",
                       Qt.Key_P:"p",Qt.Key_Q:"q",Qt.Key_R:"r",Qt.Key_S:"s",Qt.Key_T:"t",
                       Qt.Key_U:"u",Qt.Key_V:"v",Qt.Key_W:"w",Qt.Key_X:"x",Qt.Key_Y:"y",
                       Qt.Key_Z:"z"}
            if event.key() in numberMap.keys():
                pressedNumber = numberMap[event.key()]
                currentIndex = self.selectedIndexes()[0]
                for currentIndex in self.selectedIndexes():
                    currentData = self.model().itemFromIndex(currentIndex).text()
                    self.model().setData(currentIndex,currentData+str(pressedNumber))
            elif event.key() in charMap.keys():
                pressedChar = charMap[event.key()]
                currentIndex = self.selectedIndexes()[0]
                for currentIndex in self.selectedIndexes():
                    currentData = self.model().itemFromIndex(currentIndex).text()
                    self.model().setData(currentIndex,currentData+str(pressedChar))
            elif event.key() in [Qt.Key_Backspace]:
                for currentIndex in self.selectedIndexes():
                    currentData = self.model().itemFromIndex(currentIndex).text()
                    if len(currentData) >= 1:
                        self.model().setData(currentIndex,currentData[:-1])

            if event.key() in [Qt.Key_Left,Qt.Key_Right,Qt.Key_Up,Qt.Key_Down]:
                currentRow = self.selectedIndexes()[0].row()
                currentColumn = self.selectedIndexes()[0].column()
                if event.key()==Qt.Key_Left:                
                    sibling = self.selectedIndexes()[0].sibling(currentRow, currentColumn-1)
                elif event.key()==Qt.Key_Right:                
                    sibling = self.selectedIndexes()[0].sibling(currentRow, currentColumn+1)
                elif event.key()==Qt.Key_Up:                
                    sibling = self.selectedIndexes()[0].sibling(currentRow-1, currentColumn)
                elif event.key() in [Qt.Key_Down, Qt.Key_Return]:                
                    sibling = self.selectedIndexes()[0].sibling(currentRow+1, currentColumn)
                if (sibling.row(), sibling.column()) != (-1,-1):
                    self.setCurrentIndex(sibling)
        



    def c_copyContent(self):
        indexes = sorted([(itemIndex.row(),itemIndex.column()) for itemIndex in self.selectedIndexes()])
        rowRange=[indexes[0][0],indexes[-1][0]]
        colRange=[indexes[0][1],indexes[-1][1]]
        for index in indexes:
            if index[0] < rowRange[0]:
                rowRange[0] = index[0]
            if index[0] >= rowRange[1]:
                rowRange[1] = index[0]+1
            if index[1] < colRange[0]:
                colRange[0] = index[1]
            if index[1] >= colRange[1]:
                colRange[1] = index[1]+1
        text=""
        for row in range(*rowRange):
            for col in range(*colRange):
                if (row,col) in indexes:
                    text += self.model().data(self.selectedIndexes()[0].sibling(row, col))
                if col < colRange[1] - 1:
                    text+="\t"
            if row < rowRange[1] - 1:
                text+="\n"
        QApplication.clipboard().setText(text)

    def c_pasteContent(self):
        df = pd.read_clipboard(sep="\t",header=None)
        rowStart = self.selectedIndexes()[0].row()                
        colStart = self.selectedIndexes()[0].column()        
        self.model().paste_dataFrame(df,rowStart,colStart)

class TableWidget(TableView):
    def __init__(self, defaultRowDict={}, row_direction="vertical", acceptDrops=False ,parent=None):
        super().__init__(parent)
        self.setModel(TableModel(defaultRowDict=defaultRowDict, row_direction=row_direction))
        self.setAcceptDrops(acceptDrops)


def TableEditorComponent(id, label, layout, model = None):
    widget = TableView()
    layout.addWidget(widget)

    if model is not None:
        module_cls = model[0]
        model_id = model[1]
        if len(model) > 2:
            data_index = model[2]
            tableModel = module_cls().get(model_id)[data_index]
        else:
            data_index = None
            tableModel = module_cls().get(model_id)
        widget.setModel(tableModel)

