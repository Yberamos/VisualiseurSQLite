from connect_SQLite import Connection, SQLiteConnectionError
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys
from math import sqrt


# Main Window
class Visualiseur(QWidget):
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
        self.textbox.move(20,  20)
        self.textbox.resize(280, 40)

        # Create a button in the window
        self.button = QPushButton('Load tables', self)
        self.button.move(20, 80)
        self.textbox.setText("../SQLite/meals.db")

        # connect button to function on_click
        self.button.clicked.connect(self.on_click)

        # Show window
        self.show()

    def on_click(self):
        self.db_path = self.textbox.text()
        tables = []
        tables_sgbd = None

        try:
            with Connection(self.db_path) as db:
                tables_sgbd = db.get_tablesnames()
        except SQLiteConnectionError as error:
            self.textbox.setText(error.message)

        if tables_sgbd is not None:
            for tableName in tables_sgbd:
                tables.append(self.createTable(tableName))
            nbLigne = int(sqrt(len(tables)))
            nbColone = len(tables) - nbLigne
            positions = [(i, j) for i in range(nbLigne)
                         for j in range(nbColone)]

            for position, table in enumerate(tables):
                self.layout.addWidget(
                    table, positions[position][0], positions[position][1])
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

        # TODO: those ligne does nothing, how to auto stretch?
        header = tableWidget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        tableWidget.setFixedHeight(100)

        return tableWidget


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Visualiseur()
    sys.exit(app.exec_())
