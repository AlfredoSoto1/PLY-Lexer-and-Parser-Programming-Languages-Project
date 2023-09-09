import ply.lex as lex

# List of keywords
keywords = {
    'print': 'PRINT',
    'while': 'WHILE',
    'if': 'IF',
    'else': 'ELSE',
    'int': 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
}

# Token definitions
tokens = [
    'ID',
    'INT',
    'DOUBLE',
    'COMMENT',
    'WHITESPACE',
    'RO',
    'RC',
    'BO',
    'BC',
    'SO',
    'SC',
    'EQ',
    'NOT',
    'OR',
    'AND',
    'MIN',
    'MAJ',
    'MIN_EQ',
    'MAJ_EQ',
    'PLUS',
    'MINUS',
    'STAR',
    'DIV',
    'CM',
    'S'
] + list(keywords.values())

# Regular expression rules for tokens
t_ignore = ' \t\r'  # Ignore space, tab, and carriage return

def t_COMMENT(t):
    r'//[^\\n]*'
    pass  # Ignore comments

def t_WHITESPACE(t):
    r'\n'
    pass  # Newlines are ignored

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    t.type = keywords.get(t.value, 'ID')  # Check if it's a keyword
    return t

def t_DOUBLE(t):
    r'-?\d+\.\d+([Ee][+-]?\d+)?'
    return t

def t_INT(t):
    r'-?[1-9]\d*|0'
    return t

# Single-character tokens
t_RO = r'\('
t_RC = r'\)'
t_BO = r'\{'
t_BC = r'\}'
t_SO = r'\['
t_SC = r'\]'
t_EQ = r'='
t_NOT = r'!'
t_OR = r'\|'
t_AND = r'&'
t_MIN = r'<'
t_MAJ = r'>'
t_MIN_EQ = r'<='
t_MAJ_EQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'-'
t_STAR = r'\*'
t_DIV = r'/'
t_CM = r','
t_S = r';'

# Error handling
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()

# Example usage
data = '''
while (x < 10) {
    print(x);
}
'''
lexer.input(data)
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
