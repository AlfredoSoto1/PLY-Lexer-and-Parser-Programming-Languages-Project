# Using ply - lexer we are going to:
# create our custom tokens with our regular expressions.
# This later will be sent to the ply-lexer and build the 
# machine that will interpret our code. For this instance
# the machine will ONLY scan the code and tokenize all
# elements inside the test program provided as a text file

import ply.lex  as ply_lexer
import ply.yacc as ply_parser

# Create the scanner machine (lexer) to tokenize
# the given input program file (Test_program.txt)
with open('src/Test_program.txt', 'r') as source_file:
    # Obtain the source code from source file
    source_code = source_file.read() 

# --- Lexer machine parameters implementation ---

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
lexer = ply_lexer.lex()

# --- Parser machine implementation ---

# def p_expression_plus(p):
#     'expression : expression PLUS term'
#     p[0] = p[1] + p[3]

# def p_expression_minus(p):
#     'expression : expression MINUS term'
#     p[0] = p[1] - p[3]

# def p_expression_term(p):
#     'expression : term'
#     p[0] = p[1]

# def p_term_times(p):
#     'term : term STAR factor'
#     p[0] = p[1] * p[3]

# def p_term_div(p):
#     'term : term DIV factor'
#     p[0] = p[1] / p[3]

# def p_term_factor(p):
#     'term : factor'
#     p[0] = p[1]

# def p_factor_num(p):
#     '''factor : INT
#               | DOUBLE
#     '''
#     p[0] = p[1]

# def p_factor_expr(p):
#     'factor : RO expression RC'
#     p[0] = p[2]

# # Error rule for syntax errors
# def p_error(p):
#     print("Syntax error in input!")

# # Build the parser
# parser = ply_parser.yacc()

# while True:
#    try:
#        s = input(source_code)
#    except EOFError:
#        break
#    if not s: continue
#    result = parser.parse(s)
#    print(result)

# Define the parsing rules using PLY
precedence = (
    ('left', 'AND', 'OR'),
    ('nonassoc', 'EQ_EQ', 'MIN', 'MAJ', 'MIN_EQ', 'MAJ_EQ', 'EQ_MIN', 'EQ_MAJ'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV'),
    ('right', 'NOT'),
    ('left', 'RO', 'RC'),
)

def p_prog(p):
    '''
    prog : decl_list stmt_list
    '''
    # Define the action for prog
    p[0] = ('prog', p[1], p[2])

def p_decl_list_empty(p):
    '''
    decl_list : empty
    '''
    # Define the action for an empty decl_list
    p[0] = []

def p_decl_list_decl(p):
    '''
    decl_list : decl_list decl
    '''
    # Define the action for decl_list with decl
    p[0] = p[1] + [p[2]]

def p_decl(p):
    '''
    decl : type var_list S
    '''
    # Define the action for decl
    p[0] = ('decl', p[1], p[2])

def p_type(p):
    '''
    type : INT_TYPE
         | DOUBLE_TYPE
    '''
    # Define the action for type
    p[0] = ('type', p[1])

# Error rule for syntax errors
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = ply_parser.yacc()

# Parse the source code
result = parser.parse(source_code)

# Print the parse tree
print(result)

# Run & test lexical & parser machines

# Feed the lexer with the source code
lexer.input(source_code)

while True: 
    token = lexer.token()

    if not token:
        break
    print('Line->', token.lineno, token.type, token.value)
    # print(token.type, token.value, token.lineno, token.lexpos)
    # print(token)
