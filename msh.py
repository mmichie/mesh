#!/usr/bin/env python3
# uses the following encoding: utf-8
import logging
import os
import readline
import traceback
import termcolor

from mesh import config
from mesh import history
from mesh import session

from mesh.command import CommandFactory

def setup():

    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

    if not os.path.exists(config.mesh_dir):
        os.mkdir(config.mesh_dir, mode=0o700)
    
    logging.basicConfig(filename=config.mesh_dir + 'mesh.log', level=logging.DEBUG, format=FORMAT)
    readline.parse_and_bind('tab: complete')
    readline.parse_and_bind('set editing-mode vi')
    logging.info('Set readline modes')

    logging.info('Adding previous history to readline')
    previous_history = history.recorder.dump()
    for line in previous_history:
        readline.add_history(line)

def prompt():
    cwd = os.getcwd()
    if cwd == os.path.expanduser('~'):
        cwd = '~/'

    return '┌─[][' + termcolor.colored(cwd, 'cyan') + ']\n└─▪ '

def read_command():
    line = input(prompt())
    return line

def record_command(command, session_id):
    history.recorder.insert(command, session_id)
    logging.info('Recording %s' % command)

if __name__ == "__main__":

    setup()
    session = session.Session()
    command_factory = CommandFactory()

    while True:
        try:
            command = command_factory.create_command(read_command())
            command.run()
            record_command(command, session.session_id)
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

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
