from connect_SQLite import Connection
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from math import sqrt


# Main Window
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Visualiseur SQLite'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600
        
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.new_height = 0
        self.layout = QGridLayout()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20 ,  20)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.button = QPushButton('Load tables', self)
        self.button.move(20, 80)

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Show window
        self.show()

    def on_click(self):
        self.textbox.setText("../SQLite/meals.db")
        self.db_path = self.textbox.text()
        tables = []

        with Connection(self.db_path) as db:
            tables_sgbd = db.get_tablesnames()
        for tableName in tables_sgbd:
            tables.append(self.createTable(tableName))

        
        nbLigne = int(sqrt(len(tables)))
        nbColone = len(tables) - nbLigne
        positions = [(i, j) for i in range(nbLigne) for j in range(nbColone)]

        for position, table in enumerate(tables):
            self.layout.addWidget(table, positions[position][0],positions[position][1] )
        self.setLayout(self.layout)

        #self.resize(self.width,self.new_height )


    def createTable(self, tableName):
        with Connection(self.db_path) as db:
            records = db.read_from_cursor('SELECT * FROM '+tableName)
            columns = db.get_columns(tableName)

        tableWidget = QTableWidget()

        # Row count
        tableWidget.setRowCount(len(records)+1)

        # Column count
        tableWidget.setColumnCount(len(columns))

        i = 0
        for column in columns:
            tableWidget.setItem(0, i, QTableWidgetItem(column))
            j = 1
            for record in records:
                tableWidget.setItem(j, i, QTableWidgetItem(str(record[i])))
                j = j + 1

            i = i + 1

        # Table will fit the screen horizontally
        # TODO: those ligne does nothing, how to auto stretch?

        # self.new_height = self.new_height + ((len(records)+1)*100) + 10
        
        header = tableWidget.horizontalHeader()       
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        #header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        #header.setSectionResizeMode(2, QHeaderView.ResizeToContents)
        tableWidget.setFixedHeight(100)

        """
        tableWidget.setColumnWidth(1, 80)
        header = tableWidget.verticalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setStretchLastSection(True)
        

        v_header = tableWidget.verticalHeader()
        v_header.setSectionResizeMode(QHeaderView.ResizeToContents)       
        v_header.setSectionResizeMode(0, QHeaderView.Stretch)"""
        #tableWidget.resize(len(columns)*20 ,((len(records)+1)*50))
        #tableWidget.resize(20, 20)
        #tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)

        return tableWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
