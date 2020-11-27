import sqlite3
import os

# TODO: add more exception to raise when sqlite3.Error is raised


class SQLiteConnectionError(Exception):
    """Base class for connection execption"""

    def __init__(self, message=""):
        self.message = 'Connection error: ' + message


class DbNotExist(SQLiteConnectionError):
    """Error class if database does not exist"""

    def __init__(self):
        super().__init__()
        self.message = self.message + 'The file specified does not exist'


class Connection():

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type or exc_tb or exc_tb:
            if self.db_cursor:
                try:
                    self.db_cursor.close()
                except sqlite3.Error as error:
                    raise SQLiteConnectionError(
                        'Error while closing cursor: ' + error.args[0])

            if self.db_link:
                self.disconnect_from_db()

    def __init__(self, db_path):
        self.connect_to_db(db_path)
        self.create_cursor()

    def __del__(self):
        if hasattr(self, 'db_cursor'):
            try:
                self.db_cursor.close()
            except sqlite3.Error as error:
                raise SQLiteConnectionError(
                    'Error while closing cursor: ' + error.args[0])

        if hasattr(self, 'db_link'):
            self.disconnect_from_db()

    def connect_to_db(self, db_path):  # TODO: return value if error
        try:
            if os.path.isfile(db_path):
                self.db_link = sqlite3.connect(db_path)
            else:
                raise DbNotExist()

        except sqlite3.Error as error:
            raise SQLiteConnectionError(
                'Error while connecting to sqlite: ' + error.args[0])

        except DbNotExist as error:
            raise

    def create_cursor(self):  # TODO: return value if error
        try:
            self.db_cursor = self.db_link.cursor()
        except sqlite3.Error as error:
            raise SQLiteConnectionError(
                'Error while creating database cursor: ' + error.args[0])

    def read_from_cursor(self, sql_querry, sql_values=tuple()):
        querry_result = False
        try:
            self.db_cursor.execute(sql_querry, sql_values)
            querry_result = self.db_cursor.fetchall()
        except sqlite3.Error as error:
            raise SQLiteConnectionError(
                'Error while reading from cursor : ' + error.args[0])

        return querry_result

    def write_to_cursor(self, sql_query, sql_values=tuple()):  # TODO: return value
        try:
            self.db_cursor.execute(sql_query, sql_values)
        except sqlite3.Error as error:
            raise SQLiteConnectionError(
                'Error while writing to cursor : ' + error.args[0])

    def commit_to_db(self):  # TODO: return value
        try:
            self.db_link.commit()
        except sqlite3.Error as error:
            raise SQLiteConnectionError(
                'Error while commiting cursor to database : ' + error.args[0])

    def get_tablesnames(self):  # TODO: try?
        tables = []
        sql_querry = '''
            SELECT 
                name
            FROM 
                sqlite_master 
            WHERE 
                type ='table' AND 
                name NOT LIKE 'sqlite_%'
            '''

        for table in self.read_from_cursor(sql_querry):
            tables.append(table[0])

        return tables

    def get_columns(self, tableName):  # TODO: try?
        columns = []
        sql_querry = 'PRAGMA table_info(' + tableName + ')'
        for column in self.read_from_cursor(sql_querry):
            columns.append(column[1])

        return columns

    def disconnect_from_db(self):  # TODO: return value
        try:
            self.db_link.close()
        except sqlite3.Error as error:
            print('Error while disconnecting from database: ', error)
