import os
import sys
import traceback

builtin_cmds = {'cd', 'pwd',}

def prompt():
    print '%s $ ' % os.getcwd(),

def read_command():
    return sys.stdin.readline()

def parse_command(cmd_text):
    return (cmd_text, cmd_text.strip().split())

def record_command(command):
    return True

def run_builtin(cmd):
    if cmd[0] == 'cd':
        os.chdir(cmd[1])
    elif cmd[0] == 'pwd':
        print os.getcwd()

if __name__ == "__main__":
    while True:
        try:
            prompt()
            cmd_text = read_command()
            cmd_text, cmd = parse_command(cmd_text)
            record_command(cmd)

            if cmd[0] in builtin_cmds:
                run_builtin(cmd)
            else:
                #pid = subprocess.Popen(cmd_text, stdin=None, stdout=None, shell=True)
                os.system(cmd_text)
        except:
            traceback.print_exc()
