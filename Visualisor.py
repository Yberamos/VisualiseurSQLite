import logging
import sys
from logging.handlers import RotatingFileHandler
from math import sqrt

from PyQt5.QtWidgets import (QApplication, QGridLayout, QHeaderView, QLineEdit,
                             QPushButton, QTableWidget, QTableWidgetItem,
                             QWidget)

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
        self.textbox.setText("../SQLite/meals.db")

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Show window
        self.setLayout(self.layout)
        self.log.debug('Windows initialized')
        self.show()

    def on_click(self):
        self.db_path = self.textbox.text()
        tables = []
        tables_sgbd = None

        # Loading tables from SQLite
        try:
            with Connection(self.db_path) as db:
                tables_sgbd = db.get_tablesnames()
            self.log.info('Tables loaded from file ' + self.db_path)
        except SQLiteConnectionError as error:
            self.textbox.setText(error.message)
            self.log.error(error.message)

        # creating the tables and adding them to the laoyt
        if tables_sgbd is not None:
            for tableName in tables_sgbd:
                tables.append(self.createTable(tableName))
            nbLigne = int(sqrt(len(tables)))
            nbColone = len(tables) - nbLigne
            positions = [(i, j) for i in range(1, nbLigne + 1)
                         for j in range(0, nbColone)]

            for position, table in enumerate(tables):
                self.layout.addWidget(
                    table, positions[position][0], positions[position][1])
            self.setLayout(self.layout)

    def createTable(self, tableName):
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
            height = (50*len(records))
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
