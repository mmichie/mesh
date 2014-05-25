import abc
import sqlite3

import config

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
            '''CREATE TABLE IF NOT EXISTS command(
                    id integer primary key autoincrement,
                    session_id integer not null,
                    tty varchar(20) not null,
                    euid int(16) not null,
                    cwd varchar(256) not null,
                    return_code int(5) not null,
                    start_time integer not null,
                    end_time integer not null,
                    duration integer not null,
                    command varchar(1000) not null
              )'''

        self.conn = sqlite3.connect(
                config.db_filename, 
                detect_types=sqlite3.PARSE_DECLTYPES
        )

        with self.conn:
            c = self.conn.cursor()
            c.execute(command_create_sql)

    def insert(self, cmd, session_id):
        with self.conn:
            c = self.conn.cursor()
            c.execute('INSERT INTO command(session_id, tty, euid, cwd, \
                start_time, end_time, duration, command, return_code) VALUES \
                (?, ?, ?, ?, ?, ?, ?, ?, ?)', (session_id, cmd.tty, cmd.euid,
                    cmd.cwd, cmd.start_time, cmd.end_time, cmd.duration,
                    cmd.command[0], cmd.return_code))

    def dump(self):
        with self.conn:
            c = self.conn.cursor()
            return c.execute('SELECT * from history')

recorder = SQLiteHistory()
