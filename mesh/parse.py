from pyparsing import *

newline_list = Forward()
newline_list = '\n' | newline_list + '\n'

linebreak = newline_list
io_number = Word(nums) + oneOf('<', '>')

separator_op = oneOf('&', ';')
sequential_sep  = ';' +  linebreak | newline_list
separator = separator_op + linebreak | newline_list

here_end = Word(printables) # apply rule 3
io_here  = '<<' + here_end | '<<-' + here_end ;
filename = Word(printables)

io_file  = '<'  + filename | '<&' + filename | '>' +filename | '>&' + filename | '>>' + filename | '<>' + filename | '>|' + filename
io_redirect = io_file | io_number + io_file | io_here | io_number + io_here
redirect_list = Forward()
redirect_list  = io_redirect | redirect_list + io_redirect

cmd_suffix = Forward()
cmd_suffix = io_redirect | cmd_suffix + io_redirect | Word(printables) | cmd_suffix + Word(printables)
cmd_prefix = Forward()
cmd_prefix = io_redirect | cmd_prefix + io_redirect | '=' | cmd_prefix + '='
cmd_word = Word(printables)
cmd_name = Word(printables)

name = Word(printables) # Apply rule 5

and_or = Forward()
term = Forward()
term = term + separator + and_or | and_or
simple_command = cmd_prefix + cmd_word + cmd_suffix | cmd_prefix + cmd_word | cmd_prefix | cmd_name + cmd_suffix | cmd_name
compound_list  = term | newline_list + term | term + separator | newline_list + term + separator

brace_group = '{' + compound_list + '}' 
subshell = '(' + compound_list + ')'
do_group = 'do' + compound_list + 'done' # Apply rule 6

wordlist = Forward()
wordlist = wordlist + Word(printables) | Word(printables)
for_clause  = 'for' + name + linebreak + do_group | 'for' + name + linebreak + 'in' + sequential_sep + do_group | 'for' + name + linebreak + 'in' + wordlist + sequential_sep + do_group

pattern = Forward()
pattern = Word(printables) | pattern + '|' + Word(printables) #Do not apply rule 4

case_item  = pattern + ')' + linebreak + ';;' + linebreak | pattern + ')' + compound_list + ';;' + linebreak | '(' + pattern + ')' + linebreak + ';;' +  linebreak | '('  + pattern + ')' + compound_list + ';;' + linebreak
case_item_ns = pattern + ')' + linebreak | pattern + ')' + compound_list + linebreak | '(' + pattern + ')' + linebreak | '(' + pattern + ')' + compound_list + linebreak

case_list = Forward()
case_list = case_list + case_item | case_item
case_list_ns = case_list + case_item_ns | case_item_ns
case_clause = 'case' + Word(printables) + linebreak + 'in' + linebreak + case_list + 'esac' | 'case' + Word(printables) + linebreak + 'in' + linebreak + case_list_ns + 'esac' | 'case' + Word(printables) + linebreak + 'in' + linebreak + 'esac' 

else_part = Forward()
else_part = 'elif' + compound_list + 'then' + else_part | 'else' + compound_list
if_clause = 'if' + compound_list + 'then' + compound_list + else_part + 'fi' | 'if' + compound_list + 'then' + compound_list + 'fi'

while_clause = 'while' + compound_list + do_group
until_clause = 'until' + compound_list + do_group

compound_command = brace_group | subshell | for_clause | case_clause | if_clause | while_clause | until_clause

fname = Word(printables) # Apply rule 8
function_body = compound_command | compound_command + redirect_list #Apply rule
function_definition  = fname + '(' + ')' + linebreak + function_body

command  = simple_command | compound_command | compound_command + redirect_list | function_definition
pipe_sequence = Forward()
pipe_sequence  = command | pipe_sequence + '|' + linebreak + command
pipeline  = pipe_sequence | '!' + pipe_sequence
and_or = pipeline | and_or + '&&' + linebreak + pipeline | and_or + '||' + linebreak + pipeline

sh_list = Forward()
sh_list = sh_list + separator_op + and_or | and_or
complete_command = sh_list + separator | sh_list

if __name__ == "__main__":
    print command.parseString('ls -al')
    print command.parseString('ls | more')
    print command.parseString('ls &') 
    print command.parseString('ls > output')
    print command.parseString('for i in (cat i.txt); do echo $i > out; done')
