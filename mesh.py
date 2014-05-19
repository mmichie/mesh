#!/usr/bin/env python3

import logging
import os
import shutil
import sys
import readline
import traceback

from command import Command

def setup():
    mesh_dir = os.path.expanduser('~') + '/.mesh/'
    if not os.path.exists(mesh_dir):
        os.mkdir(mesh_dir, mode=0o700)
    
    logging.basicConfig(filename=mesh_dir + 'mesh.log', level=logging.DEBUG)
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    logging.info('Set readline modes')

def prompt():
    return '%s$ ' % os.getcwd()

def read_command():
    line = input(prompt())
    return line

def record_command(command):
    logging.info('Recording %s' % command)

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

    setup()

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
