import ply.lex as lex
import sys

def remove_slash(t):
  return t.replace("\\\\", "\\").replace("\(", "(").replace("\)", ")").replace("\{", "{").replace("\}", "}").replace('\"', '"').replace('\"', '"')

tokens = [
    'STATE',
    'STATES',
    'FINITE',
    'INITIAL',
    'BINDING',
    'ALPHABET',
    'TRANSITION',
    'ASSIGNMENT',
    'SYMBOL',
    'SET',
]

t_ASSIGNMENT = r'='
t_TRANSITION = r'->'
t_STATES = r'STATES'
t_FINITE = r'FINITE'
t_INITIAL = r'INITIAL'
t_ALPHABET = r'ALPHABET'
t_BINDING = r'\+\+'


t_ignore = ' \t'


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


def t_SYMBOL(t):
    r'"(([^\\]*?)|\\.)*?\"'
    t.value = remove_slash(t.value[1:-1]).replace("\,", ",")
    return t

def t_STATE(t):
    r'\((([^\\]*?)|\\.)*?\)'
    t.value = remove_slash(t.value[1:-1]).replace("\,", ",")
    return t

def t_SET(t):
    r'{(([^\\]*?)|\\.)*?}'
    t.value = remove_slash(t.value[1:-1])
    return t


lexer = lex.lex()


def main():
    lexer = lex.lex()
    rfile = open(sys.argv[1])
    input = rfile.read()
    lexer.input(input)
    wfile = open(sys.argv[1] + ".out", 'w')
    while True:
        tok = lexer.token()
        if not tok:
            break
        wfile.write(str(tok) + '\n')


if __name__ == "__main__":
    main()
