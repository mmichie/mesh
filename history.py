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

    """
    Inspired by ideas and code from: 
    https://code.google.com/p/advanced-shell-history
    Carl Anderson - 2012 - Apache License, Version 2.0 
    """

    def __init__(self):
        command_create_sql = \
            '''CREATE TABLE IF NOT EXISTS commands(
                    id integer primary key autoincrement,
                    session_id integer not null,
                    shell_level integer not null,
                    command_no integer,
                    tty varchar(20) not null,
                    euid int(16) not null,
                    cwd varchar(256) not null,
                    rval int(5) not null,
                    start_time integer not null,
                    end_time integer not null,
                    duration integer not null,
                    pipe_cnt int(3),
                    pipe_vals varchar(80),
                    command varchar(1000) not null,
                    UNIQUE(session_id, command_no)
              )'''

        db_filename = os.path.expanduser('~') + '/.mesh/history.sqlite'
        self.conn = sqlite3.connect(db_filename, detect_types=sqlite3.PARSE_DECLTYPES)

        with self.conn:
            c = self.conn.cursor()
            c.execute(command_create_sql)

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
