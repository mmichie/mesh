import abc
import datetime
import sqlite3
import os

class BaseHistory:
    __metaclass__  = abc.ABCMeta

    @abc.abstractmethod
    def insert(self, statement):
        """Insert a history item"""

    def dump(self):
        """Print entire history"""

class SQLiteHistory(BaseHistory):

    def __init__(self):

        db_filename = os.path.expanduser('~') + '/.mesh/history.sqlite'
        self.conn = sqlite3.connect(db_filename, detect_types=sqlite3.PARSE_DECLTYPES)

        with self.conn:
            c = self.conn.cursor()
            c.execute('CREATE TABLE IF NOT EXISTS history(datetime text, statement text)')

    def insert(self, statement):
        with self.conn:
            c = self.conn.cursor()
            c.execute('INSERT INTO history(datetime, statement) VALUES (?, ?)',
                    (datetime.datetime.now(), statement))

    def dump(self):
        with self.conn:
            c = self.conn.cursor()
            return c.execute('SELECT * from history')

recorder = SQLiteHistory()
