#!/usr/bin/env python3

import logging
import os
import readline
import traceback

import termcolor

from command import CommandFactory

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

    return '┌─[][' + termcolor.colored(cwd, 'cyan') + ']\n└─▪ '

def read_command():
    line = input(prompt())
    return line

def record_command(command):
    logging.info('Recording %s' % command)

if __name__ == "__main__":

    setup()

    while True:
        try:
            command = CommandFactory.create_command(read_command())
            record_command(command)
            command.run()
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
