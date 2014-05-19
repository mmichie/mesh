#!/usr/bin/env python3

import logging
import os
import sys
import readline
import traceback

from command import Command

def setup():
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    mesh_dir = os.path.expanduser('~') + '/.mesh/'
    if not os.path.exists(mesh_dir):
        os.mkdir(mesh_dir, mode=0o700)
    
    logging.basicConfig(filename=mesh_dir + 'mesh.log', level=logging.DEBUG, format=FORMAT)

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
    if command.command[0] == 'cd':
        os.chdir(command.command[1])
        logging.debug('Built in chdir to: %s' % command.command[1])
    elif command.command[0] == 'pwd':
        print(os.getcwd())
        logging.debug('Built in pwd')
    elif command.command[0] == 'exit':
        logging.debug('Built in exit')
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
            logging.exception('Uncaught exception')
            traceback.print_exc()
