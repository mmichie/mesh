#!/usr/bin/env python3

import os
import shutil
import sys
import readline
import traceback

from command import Command

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')

def prompt():
    return '%s$ ' % os.getcwd()

def read_command():
    line = input(prompt())
    return line

def record_command(command):
    return True

def run_builtin(command):
    if shutil.which(command.command[0]):
        os.system(command.text)
    elif command.command[0] == 'cd':
        os.chdir(command.command[1])
    elif command.command[0] == 'pwd':
        print(os.getcwd())
    elif command.command[0] == 'exit':
        sys.exit()

if __name__ == "__main__":
    while True:
        try:
            command = Command(read_command())
            record_command(command)

            if command.builtin():
                run_builtin(command)
            else:
                os.system(command.alias)
        except KeyboardInterrupt:
            print('')
            pass
        except SystemExit:
            break
        except EOFError:
            print('')
            break
        except:
            traceback.print_exc()
