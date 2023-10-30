import ply.lex  as ply_lexer
import ply.yacc as ply_parser

# Create the scanner machine (lexer) to tokenize
# the given input program file (Test_program.txt)
with open('src/Test_program.txt', 'r') as source_file:
    # Obtain the source code from source file
    source_code = source_file.read() 

source_code = """
int x, y, z;
int b[2][2][2];
double a;
a = 10;
b[1][1][1] = 0;

x = 10;
y = 20;
z = 30;

// a = a-1;
// a = a - 1;
// a = a + a + -a + -1;
// a = a + - 1; // not compile
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
    'INT',         # consists of: -?[0-9]+
    'DOUBLE',      # consists of: -?[0-9]+\.([0-9]+)?
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
    'UMINUS',   # unitary minus (-)
    'MINUS_ID', # unitary minus on IDs (-)
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

def t_MINUS_ID(t):
    r'\-[a-zA-Z][a-zA-Z0-9]*'
    t.value = t.value[1:]  # Remove the minus sign  
    return t

def t_ID(t):
    r'[a-zA-Z][a-zA-Z0-9]*'
    # Check if it's a keyword
    t.type = defined_keywords.get(t.value, 'ID')  
    return t

def t_UMINUS(t):
    r'[-]\d+(\.\d+)?'
    t.value = float(t.value) if '.' in t.value else int(t.value)
    return t

def t_MINUS(t):
    r'\-'
    return t

def t_DOUBLE(t):
    r'[0-9]+\.([0-9]+)?'
    return t

def t_INT(t):
    r'[0-9]+'
    t.value = int(t.value)
    return t

# Error handling
def t_error(t):
    pass

# Build the lexer
lexer = ply_lexer.lex()

# Feed the lexer with the source code
lexer.input(source_code)

print('--------------Lexical stage----------------')

while True: 
    token = lexer.token()

    if not token:
        break
    print('Line->', token.lineno, token.type, token.value)
    # print(token.type, token.value, token.lineno, token.lexpos)
    # print(token)

print('--------------Parser stage----------------')

# --- Parser machine implementation ---

assembly_code = []

def generate_array_index_code(index_array):
    array_indices = ""
    for var in index_array[1:]:
        array_indices += "[" + str(var) + "]"
    return array_indices

precedence = (
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV'),
    ('right', 'UMINUS'),
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
    for variable in p[2]:
        assembly_code.append(f'{p[1]} {variable[0]}{generate_array_index_code(variable)}')
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
    '''assignment : id EQ exp S'''
    id_index_array = p[1]
    if isinstance(id_index_array, list):
        # If it's an array access
        assembly_code.append(f'EVAL {p[3]}')
        assembly_code.append(f'ASS {id_index_array[0]}{generate_array_index_code(id_index_array)}')
    else:
        # If it's a simple identifier
        assembly_code.append(f'EVAL {p[3]}')
        assembly_code.append(f'ASS {id_index_array}')
    pass

def p_type(p):
    '''type : INT_TYPE
        | DOUBLE_TYPE
    '''
    if p[1] == 'int':
        p[0] = 'INT'
    elif p[1] == 'double':
        p[0] = 'DOUBLE'
    pass

def p_var_list(p):
    '''var_list : var
        | var_list CM var
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
    pass

def p_var(p):
    '''var : ID array'''
    if p[2] is None:
        p[0] = p[1]
    else:
        p[0] = [p[1]] + p[2]
    pass

def p_array(p):
    '''array : empty
        | SO INT SC array
    '''
    if len(p) == 5:
        # Non-empty id_array
        if p[4] is None:
            p[0] = [p[2]]
        else:
            p[0] = [p[2]] + p[4]
    else:
        # Empty id_array
        p[0] = None
    pass

def p_id_array(p):
    '''id_array : SO INT SC id_array
        | SO id SC id_array
        | empty
    '''
    if len(p) == 5:
        # Non-empty id_array
        if p[4] is None:
            p[0] = [p[2]]
        else:
            p[0] = [p[2]] + p[4]
    else:
        # Empty id_array
        p[0] = None
    pass

def p_id(p):
    '''id : ID
        | ID id_array
    '''
    if len(p) == 2:
        # Pass the ID only
        p[0] = p[1]
    else:
        if p[2] is not None:
            p[0] = [p[1]] + p[2]
        else:
            p[0] = [p[1]]
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
        | exp UMINUS
        | exp MINUS_ID
        | RO exp RC
        | id
        | INT
        | DOUBLE
        | UMINUS
        | MINUS_ID
    '''
    if len(p) == 2:
        p[0] = p[1]
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

# print the generated assembly code
print('--------------Pseudo-assembly code----------------')
for code in assembly_code:
    print(code)