#!/usr/bin/env python3

import os
import shutil
import sys
import readline
import traceback

from alias import aliases

readline.parse_and_bind('tab: complete')
readline.parse_and_bind('set editing-mode vi')
builtin_cmds = {'cd', 'pwd', 'exit', 'alias',}

def prompt():
    return '%s$ ' % os.getcwd()

def read_command():
    line = input(prompt())
    return line

def parse_command(cmd_text):
    return (cmd_text, cmd_text.strip().split())

def record_command(command):
    return True

def substitute_alias(cmd, cmd_text):
    if cmd[0] in aliases.keys():
        return aliases[cmd[0]] + ' ' + ' '.join(cmd[1:])
    else:
        return cmd_text

def run_builtin(cmd, cmd_text):
    if shutil.which(cmd[0]):
        os.system(cmd_text)
    elif cmd[0] == 'cd':
        os.chdir(cmd[1])
    elif cmd[0] == 'pwd':
        print(os.getcwd())
    elif cmd[0] == 'exit':
        sys.exit()

if __name__ == "__main__":
    while True:
        try:
            cmd_text = read_command()
            cmd_text, cmd = parse_command(cmd_text)
            cmd_text = substitute_alias(cmd, cmd_text)
            record_command(cmd)

            if cmd[0] in builtin_cmds:
                run_builtin(cmd, cmd_text)
            else:
                os.system(cmd_text)
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
