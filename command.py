
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

