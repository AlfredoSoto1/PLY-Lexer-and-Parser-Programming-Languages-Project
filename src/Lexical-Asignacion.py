# Using ply - lexer we are going to:
# create our custom tokens with our regular expressions.
# This later will be sent to the ply-lexer and build the 
# machine that will interpret our code. For this instance
# the machine will ONLY scan the code and tokenize all
# elements inside the test program provided as a text file

# import ply lexer
import ply.lex as lex

# List of keywords
defined_keywords = {
    'print' : 'PRINT',
    'while' : 'WHILE',
    'if'    : 'IF',
    'else'  : 'ELSE',
    'int'   : 'INT_TYPE',
    'double': 'DOUBLE_TYPE',
}

# Declaration of the assigned tokens
# for lexer from ply to use when scanning the code
tokens = [
    'ID',          # consists of: [a-zA-Z][a-zA-Z0-9]*
    'INT',         # consists of: -?[1-9][0-9]*
    'DOUBLE',      # consists of: -?[0-9]+(\.[0-9]+)?([Ee][+-]?[0-9]+)?
    'COMMENT',     # consists of: //[.*]\n
    'WHITESPACE',  # consists of: [ \t\r]+
    'NEWLINE',     # consists of: [\n]+
    
    # Delimeters represented in string
    'RO',          # (
    'RC',          # )
    'BO',          # {
    'BC',          # }
    'SO',          # [
    'SC',          # ]

    # Operators represented in string
    'EQ',       # =
    'NOT',      # ! 
    'OR',       # |
    'AND',      # &
    'MIN',      # <
    'MAJ',      # >
    'MIN_EQ',   # <=
    'MAJ_EQ',   # >=
    'PLUS',     # +
    'MINUS',    # -
    'STAR',     # *
    'DIV',      # /
    'CM',       # ,
    'S'         # ;
] + list(defined_keywords.values())

# Single-character tokens
# Regular expression rules
t_RO = r'\('
t_RC = r'\)'
t_BO = r'\{'
t_BC = r'\}'
t_SO = r'\['
t_SC = r'\]'
t_EQ = r'='
t_NOT = r'!'
t_OR = r'\|'
t_AND = r'\&'
t_MIN = r'<'
t_MAJ = r'>'
t_MIN_EQ = r'<='
t_MAJ_EQ = r'>='
t_PLUS = r'\+'
t_MINUS = r'\-'
t_STAR = r'\*'
t_DIV = r'/'
t_CM = r','
t_S = r';'

def t_COMMENT(t):
    r'//.*\n' # Ignore comments
    pass

def t_WHITESPACE(t):
    r'[ \t\r]+' # ignore spaces, tabs and carriage
    pass

def t_NEWLINE(t):
    r'[\n]+'
    # calculate line number
    t.lexer.lineno += len(t.value)
    pass

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    # Check if it's a keyword
    t.type = defined_keywords.get(t.value, 'ID')  
    return t

def t_DOUBLE(t):
    r'-?[0-9]+(\.[0-9]+)?([Ee][+-]?[0-9]+)?'
    return t

def t_INT(t):
    r'-?[1-9][0-9]*'
    return t

# Error handling
def t_error(t):
    pass

# Build the lexer
lexer = lex.lex()

# Create the scanner machine (lexer) to tokenize
# the given input program file (Test_program.txt)
with open('src/Test_program.txt', 'r') as source_file:
    # Obtain the source code from source file
    source_code = source_file.read() 

# Feed the lexer with the source code
lexer.input(source_code)

while True: 
    token = lexer.token()

    if not token:
        break

    
    # print('Line->', token.lineno, token.type, token.value)
    # print(token.type, token.value, token.lineno, token.lexpos)
    # print(token)