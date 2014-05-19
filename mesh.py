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
    cwd = os.getcwd()
    if cwd == os.path.expanduser('~'):
        cwd = '~/'

    return '%s$ ' % cwd

def read_command():
    line = input(prompt())
    return line

def record_command(command):
    logging.info('Recording %s' % command)

def run_builtin(command):
    if command.command[0] == 'cd':
        prev_cwd = os.getcwd()

        # no point in doing work if you don't give us a place to go
        if len(command.command) <2:
            return

        if command.command[1] == '-':
            if 'OLDPWD' in os.environ:
                os.chdir(os.environ['OLDPWD'])
            else:
                print('No previous directory set')
        elif command.command[1] == '~':
            os.chdir(os.path.expanduser('~'))
        else:
            os.chdir(command.command[1])

        os.environ['OLDPWD'] = prev_cwd
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
