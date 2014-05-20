import logging
import os
import shutil
import sys

from alias import aliases

builtin_cmds = {'cd', 'pwd', 'exit', 'alias', 'echo',}

class Command:
 
    def __init__(self, command_text):
        self.text = command_text
        self.command = self.parse_command(command_text)
        self.alias = self.substitute_alias()

    def __str__(self):
        return self.text

    def parse_command(self, command_text):
        return command_text.strip().split()

    def substitute_alias(self):
        if self.command[0] in aliases.keys():
            return aliases[self.command[0]] + ' ' + ' '.join(self.command[1:])
        else:
            return self.text

    def builtin(self):
        if self.command[0] in builtin_cmds:
            return True
        else:
            return False

    def run(self):
        os.system(self.alias)

class NullCommand(Command):
    def __init__(self, command_text):
        self.text = command_text
        self.command = ['']
        self.alias = ''

    def run(self):
        pass

class Builtin(Command): pass

class EchoBuiltin(Builtin):
    def run(self):
        if shutil.which('echo'):
            os.system(self.text)
            logging.debug('Using system echo')
        else:
            print(' '.join(self.command[1:]))
            logging.debug('Built in echo')

class ChangeDirectoryBuiltin(Builtin):
    def run(self):
        prev_cwd = os.getcwd()

        # no point in doing work if you don't give us a place to go
        if len(self.command) <2:
            return

        if self.command[1] == '-':
            if 'OLDPWD' in os.environ:
                os.chdir(os.environ['OLDPWD'])
            else:
                print('No previous directory set')
        elif self.command[1] == '~':
            os.chdir(os.path.expanduser('~'))
        else:
            os.chdir(self.command[1])

        os.environ['OLDPWD'] = prev_cwd
        logging.debug('Built in chdir to: %s' % self.command[1])

class PrintWorkingDirectoryBuiltin(Builtin):
    def run(self):
        print(os.getcwd())
        logging.debug('Built in pwd')

class ExitBuiltin(Builtin):
    def run(self):
        sys.exit()
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

