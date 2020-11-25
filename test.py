from my_sqlite3 import MyConnection
from PyQt5.QtWidgets import *
import sys



#Main Window 
class App(QWidget): 
    def __init__(self, db_path): 
        super().__init__() 
        self.title = 'PyQt5 - QTableWidget'
        self.left = 0
        self.top = 0
        self.width = 500
        self.height = 700
        self.tables = []
        self.setWindowTitle(self.title) 
        self.setGeometry(self.left, self.top, self.width, self.height) 
        with MyConnection(db_path) as db:
            tables_sgbd = db.get_tablesnames()
        
        for tableName in tables_sgbd:
            self.tables.append(self.createTable(tableName))
   
        self.layout = QVBoxLayout() 

        for table in self.tables:
            self.layout.addWidget(table) 
        self.setLayout(self.layout) 
   
        #Show window 
        self.show() 
   
    #Create table 
    def createTable(self, tableName): 
        with MyConnection(db_path) as db:
            records = db.read_from_cursor('SELECT * FROM '+tableName)
            columns = db.get_columns(tableName)

        tableWidget = QTableWidget() 
  
        #Row count 
        tableWidget.setRowCount(len(records)+1)  
  
        #Column count 
        tableWidget.setColumnCount(len(columns))   

        i = 0
        for column in columns:
            tableWidget.setItem(0,i, QTableWidgetItem(column))
            j = 1
            for record in records:
                print(type(record[i]))
                tableWidget.setItem(j,i, QTableWidgetItem(str(record[i])))
                j = j + 1
            
            i = i + 1
 
        #Table will fit the screen horizontally 
        # TODO: those ligne does nothing, how to auto stretch?
        tableWidget.horizontalHeader().setStretchLastSection(True) 
        tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) 
        
        return tableWidget
   
if __name__ == '__main__': 
    db_path='../SQLite/meals.db'
    app = QApplication(sys.argv) 
    ex = App(db_path) 
    sys.exit(app.exec_()) 