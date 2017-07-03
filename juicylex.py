"""
juicylang - Juicy programming language written in Python using PLY
Author : Hamidreza Mahdavipanah
Version: 1.0.0
Repository: http://github.com/mahdavipanah/juicylang
License : MIT License
"""
from colorama import init as colorama_init, Fore
from re import UNICODE as RE_UNICODE
import ply.lex as lex

# Initialize colorama
colorama_init(autoreset=True)


# Computes column
#     t is a token instance
def find_column(t):
    last_cr = t.lexer.lexdata.rfind('\n', 0, t.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (t.lexpos - last_cr) + 1
    return column


# Prints an error output for illegal token
def token_error(t):
    print(Fore.RED + ("Illegal character '" + Fore.BLACK + "{}" + Fore.RED + "' in line {} column {}").format(
        t.value[0], t.lineno, find_column(t))
          )
    t.lexer.skip(1)


# Track line numbers
def token_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# Juicy's reserved keywords
reserved = {
    'if': 'IF',
    'else': 'ELSE',
    'while': 'WHILE',
    'input': 'INPUT',
    'print': 'PRINT',
    'len': 'LEN',
    'to_str': 'TO_STR',
    'err': 'ERR',
    'to_int': 'TO_INT',
    'to_float': 'TO_FLOAT',
    'and': 'AND',
    'or': 'OR',
    'not': 'NOT',
}

# Juicy's tokens
tokens = (
             'NOTEQUAL',
             'GE',
             'LE',
             'ASSIGN',
             'SYMBOL',
             'FLOAT',
             'INT',
             'STRING',
         ) + tuple(reserved.values())

t_NOTEQUAL = r'<>'
t_ASSIGN = r':='

literals = (
    '>',
    '<',
    '=',
    '+',
    '-',
    '*',
    '/',
    '^',
    '{',
    '}',
    '[',
    ']',
    '(',
    ')',
    ':',
    ';',
    ',',
)

# Juicy's lexer states
states = (
    ('comment', 'exclusive'),
)


t_GE = r'>='
t_LE = r'<='


# Opening of first comment
def t_LCOMM(t):
    r'\/\*'
    t.lexer.comment_level = 1
    t.lexer.begin('comment')


# Opening of first nested comment
def t_comment_LCOMM(t):
    r'\/\*'
    t.lexer.comment_level += 1


# Ignore everything inside a comment
t_comment_ignore_contents = r'[\s\S]'
# Just for removing PLY's warning
t_comment_ignore = ''


# Closing a comment
def t_comment_RCOMM(t):
    r'\*\/'
    t.lexer.comment_level -= 1

    # If it was the most outer comment closing
    if t.lexer.comment_level == 0:
        t.lexer.begin('INITIAL')


t_comment_newline = token_newline

t_comment_error = token_error


# Read in a float. This rule has to be done before the int rule.
def t_FLOAT(t):
    r'\d+\.\d*(e-?\d+)?'
    t.value = float(t.value)
    return t


# Read in an int
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# Read in a string, as in C. The following backslash sequences have their usual special meaning: \", \\, \n, and \t
def t_STRING(t):
    r'\"([^\\"]|(\\.))*\"'
    escaped = 0
    # Remove first and last double quotations
    old_str = t.value[1:-1]
    new_str = ""
    for i in range(0, len(old_str)):
        c = old_str[i]
        if escaped:
            if c == "n":
                c = "\n"
            elif c == "t":
                c = "\t"
            new_str += c
            escaped = 0
        else:
            if c == "\\":
                escaped = 1
            else:
                new_str += c
    t.value = new_str
    return t


# Read in a symbol. This rule must be practically last since there are so
# few rules concerning what constitutes a symbol
def t_SYMBOL(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    # See if symbol is a reserved keyword
    t.type = reserved.get(t.value, 'SYMBOL')
    return t


t_newline = token_newline

t_ignore = ' \t'

t_error = token_error

# Build the lexer
lex.lex(reflags=RE_UNICODE)

if __name__ == '__main__':
    lex.runmain()
