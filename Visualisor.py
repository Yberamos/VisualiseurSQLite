import logging
import sys
from logging.handlers import RotatingFileHandler
from math import sqrt

from PyQt5.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QWidget, QLabel)

from connect_SQLite import Connection, SQLiteConnectionError


# Main Window
class Visualiseur(QWidget):
    def __init__(self):
        super().__init__()
        # Start logger
        self.log = logging.getLogger('Visualiseur')
        handler = RotatingFileHandler('./Visualisor_log.log')
        formater = logging.Formatter(
            '%(asctime)s :: %(levelname)s :: %(message)s', '%Y-%m-%d %H:%M:%S')
        self.log.setLevel(logger_level)
        handler.setFormatter(formater)
        self.log.addHandler(handler)
        self.title = 'Visualiseur SQLite'
        self.left = 0
        self.top = 0
        self.width = 800
        self.height = 600

        self.setWindowTitle(self.title)
        #self.setGeometry(self.left, self.top, self.width, self.height)
        self.new_height = 0
        self.layout = QGridLayout()

        # Create textbox
        self.textbox = QLineEdit(self)
        self.layout.addWidget(self.textbox, 0, 0)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.button = QPushButton('Load tables', self)
        self.layout.addWidget(self.button, 0, 1)
        self.textbox.setText("../Labo-Programation/meals.db")

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Show window
        self.setLayout(self.layout)
        self.log.debug('Windows initialized')
        self.show()

    def on_click(self):
        self.db_path = self.textbox.text()
        tables = {}
        tables_names = None

        # Loading tables from SQLite
        try:
            with Connection(self.db_path) as db:
                tables_names = db.get_tablesnames()
                
            self.log.info('Tables loaded from file ' + self.db_path)
        except SQLiteConnectionError as error:
            self.textbox.setText(error.message)
            self.log.error(error.message)

        # creating the tables and adding them to the laoyt
        if tables_names is not None:
            for index, tableName in enumerate(tables_names):
                print(tableName, index +1 )
                tables[tableName]={}
                tables[tableName]['widget_table'] = self.createTable(tableName)
                tables[tableName]['widget_label'] = self.createLabel(tableName)
                tables[tableName]['index'] = index + 1
            nbLigne = int(sqrt(len(tables))) 
            nbColone = len(tables) - nbLigne
            nbLigne = nbLigne *2 
            positions = [(i, j) for i in range(1, nbLigne + 1)
                         for j in range(0, nbColone)]
            # [(1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1), (4, 0), (4, 1)]

            for table in tables:
                # print('position')
                index_table = tables[table]['index']
                index_label = tables[table]['index'] - 1
                if index_table % 2 == 1:
                    index_table = index_table * 2
                else:
                    index_table = (index_table * 2)-1
                print(index_table)
                self.layout.addWidget(tables[table]['widget_table'], positions[index_table][0], positions[index_table][1])
                #self.layout.addWidget(tables[table]['widget_label'], positions[index_label][0], positions[index_label][1])


            self.setLayout(self.layout)


    def createLabel(self, tableName):
        labelWidget = QLabel()
        labelWidget.setText(tableName)
        return labelWidget

    def createTable(self, tableName): # TODO : add labbel with table name
        with Connection(self.db_path) as db:
            records = db.read_from_cursor('SELECT * FROM '+tableName)
            columns = db.get_columns(tableName)

        tableWidget = QTableWidget()
        tableWidget.setMinimumWidth(350)

        tableWidget.setRowCount(len(records))
        tableWidget.setColumnCount(len(columns))

        tableWidget.setHorizontalHeaderLabels(columns)

        # Populate the table
        for i in range(len(columns)):
            for j, record in enumerate(records):
                tableWidget.setItem(j, i, QTableWidgetItem(str(record[i])))

        # Set width
        header = tableWidget.horizontalHeader()
        for position in range(len(columns)-1):
            header.setSectionResizeMode(position, QHeaderView.ResizeToContents)

        # Set fix height
        if len(records) != 0:
            height = (30*len(records))
        else:
            height = 50

        tableWidget.setFixedHeight(height)
        self.log.debug('Table headers: ' + ', '.join(map(str, columns)))
        self.log.debug('Table records: ' + ', '.join(map(str, records)))
        return tableWidget


if __name__ == '__main__':
    logger_level = logging.DEBUG
    app = QApplication(sys.argv)
    ex = Visualiseur()
    sys.exit(app.exec_())
