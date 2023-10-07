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

source_code = """
double x[5];
int i, j;
double swap;
int pos;

// Bubble sort
pos = 5;
while (pos > 0) {
  i = 0;
  while (i < pos - 1){
    j = i + 1;
    if (x[i] > x[j]){
      swap = x[j];
      x[j] = x[i];
      x[i] = swap;
    }
    i = i + 1;
  }
  pos = pos -1;
}

// if ( pos > 0) {
//   x[0] = 3.4;
// } else {
//   x[0] = 3.7;
// }

// Print Results
 // i = 0;
 // while(i<5){
 // print x[i];
 // i = i + 1;
 // }
"""

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
    r'-?[0-9]+\.([0-9]+)?'
    return t

def t_INT(t):
    r'-?[0-9]+'
    t.value = int(t.value)
    return t

# Error handling
def t_error(t):
    pass

# Build the lexer
lexer = ply_lexer.lex()

# Feed the lexer with the source code
lexer.input(source_code)

while True: 
    token = lexer.token()

    if not token:
        break
    print('Line->', token.lineno, token.type, token.value)
    # print(token.type, token.value, token.lineno, token.lexpos)
    # print(token)


# --- Parser machine implementation ---

precedence = (
   ('left', 'PLUS', 'MINUS'),
   ('left', 'STAR', 'DIV'),
)

def p_prog(p):
    '''prog : decl_list stmt_list'''
    pass

def p_decl_list(p):
    '''decl_list : empty
        | decl_list decl
    '''
    pass

def p_empty(p):
    'empty :'
    pass

def p_decl(p):
    '''decl : type var_list S'''
    pass

def p_stmt_list(p):
    '''stmt_list : stmt_list stmt
        | stmt
    '''
    pass

def p_stmt(p):
    '''stmt : IF RO exp RC stmt
        | ELSE stmt
        | WHILE RO exp RC stmt
        | assignment
        | PRINT exp S
        | BO stmt_list BC
    '''
    pass

def p_assignment(p):
    '''assignment : id S
        | id EQ exp S
    '''
    pass

def p_type(p):
    '''type : INT_TYPE
        | DOUBLE_TYPE
    '''
    pass

def p_var_list(p):
    '''var_list : var
        | var_list CM var
    '''
    pass

def p_var(p):
    '''var : ID array'''
    pass

def p_array(p):
    '''array : empty
        | array SO INT SC
    '''
    pass

def p_id(p):
    '''id : ID
        | ID SO INT SC
        | ID SO ID SC
    '''
    pass

def p_exp(p):
    '''exp : exp AND exp
        | exp OR exp
        | NOT exp
        | exp EQ EQ exp
        | exp MIN exp
        | exp MAJ exp
        | exp MAJ_EQ exp
        | exp MIN_EQ exp
        | exp PLUS exp
        | exp MINUS exp
        | exp STAR exp
        | exp DIV exp
        | RO exp RC
        | id
        | INT
        | DOUBLE
    '''
    pass

def p_error(p):
    print(f"Syntax error at line {p.lineno}, position {p.lexpos}, token {p.type}")
    # print("Syntax error somewhere")

# Build the parser
parser = ply_parser.yacc()

# Parse the source code
result = parser.parse(source_code)

# Print the parse tree
print(result)