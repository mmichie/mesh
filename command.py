import logging
import os
import shutil
import shlex
import sys
import time

import config

from alias import aliases

builtin_cmds = {'cd', 'pwd', 'exit', 'alias', 'echo',}

class Command:
 
    def __init__(self, command_text):
        self.text = command_text
        self.parsed = self.parse_command(command_text)
        self.command = self.parsed[0]
        self.args = [] if len(self.parsed) < 2 else self.parsed[1:]
        self.alias = self.substitute_alias()

        self.command_line = self.text
        self.tty = os.ttyname(sys.stdin.fileno())
        self.euid = os.geteuid()
        self.cwd = os.getcwd()

    def __str__(self):
        return self.text

    def parse_command(self, command_text):
        return shlex.split(command_text)

    def substitute_alias(self):
        if self.command in aliases.keys():
            return aliases[self.command] + ' ' + ' '.join(self.args)
        else:
            return self.text

    def builtin(self):
        if self.command in builtin_cmds:
            return True
        else:
            return False

    def run(self):
        self.start_time = time.time()

        if config.no_fork_mode:
            logging.debug('Running through system shell')
            self.return_code = os.system(self.alias)
        else:
            logging.debug('Running through fork/exec')
            pid = os.fork()
            
            if pid: # parent
                os.waitpid(pid, 0)
            else: # child
                os.execvp(self.command, (self.command,) + tuple(self.alias.split()[1:]))

        self.return_code = 0
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time

class NullCommand(Command):
    def __init__(self, command_text):
        self.text = command_text
        self.command = ''
        self.args = []
        self.alias = ''
        self.tty = os.ttyname(sys.stdin.fileno())
        self.euid = os.geteuid()
        self.cwd = os.getcwd()
        self.start_time = time.time()

    def run(self):
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.return_code = 0

class Builtin(Command): pass

class EchoBuiltin(Builtin):
    def run(self):
        self.start_time = time.time()
        if shutil.which('echo'):
            os.system(self.text)
            logging.debug('Using system echo')
        else:
            print(' '.join(self.command[1:]))
            logging.debug('Built in echo')

        self.return_code = 0
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time

class ChangeDirectoryBuiltin(Builtin):
    def run(self):
        self.start_time = time.time()
        prev_cwd = os.getcwd()

        # return home toto
        if len(self.args) == 0:
            os.chdir(os.path.expanduser('~'))
            self.args.append('~')
        elif self.args[0] == '-':
            if 'OLDPWD' in os.environ:
                os.chdir(os.environ['OLDPWD'])
            else:
                print('No previous directory set')
        elif self.args[0].startswith('~'):
            os.chdir(os.path.expanduser('~') + '/' + self.args[0][2:])
        else:
            os.chdir(self.args[1])

        os.environ['OLDPWD'] = prev_cwd
        self.return_code = 0
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        logging.debug('Built in chdir to: %s' % self.args[0])

class PrintWorkingDirectoryBuiltin(Builtin):
    def run(self):
        self.start_time = time.time()
        print(os.getcwd())
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.return_code = 0
        logging.debug('Built in pwd')

class ExitBuiltin(Builtin):
    def run(self):
        self.start_time = time.time()
        sys.exit()
        self.end_time = time.time()
        self.duration = self.end_time - self.start_time
        self.return_code = 0
        logging.debug('Built in exit')

class CommandFactory:

    def create_command(command_text):
        command_split = command_text.split()

        if len(command_split) == 0:
            return NullCommand(command_text)
        elif command_split[0] == 'cd':
            return ChangeDirectoryBuiltin(command_text)
        elif command_split[0] == 'pwd':
            return PrintWorkingDirectoryBuiltin(command_text)
        elif command_split[0] == 'exit':
            return ExitBuiltin(command_text)
        elif command_split[0] == 'echo':
            return EchoBuiltin(command_text)
        else:
            return Command(command_text)

