import os
import pwd
import sqlite3
import socket
import sys
import time

from . import config
from . import util

class Session:

    """
    Inspired by ideas and code from: 
    https://code.google.com/p/advanced-shell-history
    Carl Anderson - 2012 - Apache License, Version 2.0 
    """

    def __init__(self):
        session_create_sql = \
            '''CREATE TABLE IF NOT EXISTS session (
                    id integer primary key autoincrement,
                    hostname varchar(128),
                    host_ip varchar(40),
                    ppid int(5) not null,
                    pid int(5) not null,
                    time_zone str(3) not null,
                    start_time integer not null,
                    end_time integer,
                    duration integer,
                    tty varchar(20) not null,
                    uid int(16) not null,
                    euid int(16) not null,
                    login varchar(48),
                    sudo_user varchar(48),
                    sudo_uid int(16),
                    ssh_client varchar(60),
                    ssh_connection varchar(100)
            )'''

        self.conn = sqlite3.connect(
                config.db_filename,
                detect_types=sqlite3.PARSE_DECLTYPES)

        with self.conn:
            c = self.conn.cursor()
            c.execute(session_create_sql)

        self.session = dict(
            euid = os.geteuid(),
            host_ip = util.get_local_ip(),
            hostname = socket.gethostname(),
            login = pwd.getpwuid(os.getuid())[0],
            pid = os.getpid(),
            ppid = os.getppid(),
            ssh_client = os.environ.get('SSH_CLIENT'),
            ssh_connection = os.environ.get('SSH_CONNECTION'),
            start_time = int(time.time()),
            sudo_uid = os.environ.get('SUDO_UID'),
            sudo_user = os.environ.get('SUDO_USER'),
            time_zone = time.tzname[time.localtime()[8]],
            tty = os.ttyname(sys.stdin.fileno()),
            uid = os.getuid(),
        )

        with self.conn:
            c = self.conn.cursor()
            query_str = "INSERT INTO session({}) VALUES({})"
            columns, values = zip(*self.session.items())
            q = query_str.format(",".join(columns),",".join("?"*len(values)))
            c.execute(q, values)
            self.session_id = c.lastrowid

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
