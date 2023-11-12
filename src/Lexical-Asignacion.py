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

while (pos > 0) {
    while (pos > 0) {
        print(3);
    }
}

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
# 'PRINT',
#     'while' : 'WHILE',
#     'if'    : 'IF',
#     'else'  : 'ELSE',
#     'int'   : 'INT_TYPE',
#     'double': 'DOUBLE_TYPE',

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

label_count = 0
assembly_code = []

precedence = (
    ('nonassoc', 'MIN', 'MAJ', 'MIN_EQ', 'MAJ_EQ'),  # Nonassociative operators
    ('left', 'PLUS', 'MINUS'),
    ('left', 'STAR', 'DIV'),
    ('right', 'UMINUS'),
    ('nonassoc', 'RO', 'RC')
)

def p_prog(p):
    '''prog : decl_list stmt_list'''
    assembly_code.append(p[1])
    assembly_code.append(p[2] + ' END')
    pass

def p_decl_list(p):
    '''decl_list : empty
        | decl decl_list
    '''
    if p[1] == None:
        p[0] = None
    elif p[2] == None:
        p[0] = f'{p[1]}'
    else:
        p[0] = f'{p[1]}\n{p[2]}'
    pass

def p_empty(p):
    'empty :'
    pass

def p_decl(p):
    '''decl : type var_list S'''
    decl_instructions = ''
    for variable in p[2]:
        decl_instructions += p[1] + ' ' +  variable + '\n'
    decl_instructions = decl_instructions.rstrip('\n')

    p[0] = decl_instructions
    pass

def p_stmt_list(p):
    '''stmt_list : stmt stmt_list
        | stmt
    '''
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[1] + '\n' + p[2]
    pass

def p_stmt(p):
    '''stmt : if_stmt
            | while_stmt
            | block_stmt
            | print_stmt
            | assignment
    '''
    p[0] = p[1] # pass the statement up
    pass

def p_if_stmt(p):
    '''if_stmt : IF RO exp RC stmt else_stmt
    '''
    global label_count
    if p[6] == None:
        p[0] = f'    EVAL {p[3]}\n    GOTOF L{label_count + 1}\n{p[5]}\nL{label_count + 1}:'
    else:
        p[0] = f'    EVAL {p[3]}\n    GOTOF L{label_count + 1}\n{p[5]}\n    GOTO L{label_count + 2}\nL{label_count + 1}:\n{p[6]}\nL{label_count + 2}:'
    label_count += 2
    pass

def p_else_stmt(p):
    '''else_stmt : ELSE stmt
            | empty
    '''
    if p[1] == None:
        p[0] = None
    else:
        p[0] = p[2]
    pass

def p_while_stmt(p):
    '''while_stmt : WHILE RO exp RC stmt
    '''
    global label_count
    p[0] = f'L{label_count}: EVAL {p[3]}\n    GOTOF L{label_count + 1}\n{p[5]}\n    GOTO L{label_count}\nL{label_count + 1}:'
    label_count += 2
    pass

def p_print_stmt(p):
    '''print_stmt : PRINT exp S
    '''
    p[0] = f'    PRINT {p[2]}'
    pass

def p_block_stmt(p):
    '''block_stmt : BO stmt_list BC
    '''
    p[0] = p[2]
    pass

def p_assignment(p):
    '''assignment : id EQ exp S'''
    p[0] = f'    EVAL {p[3]}\n    ASS  {p[1]}'
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
        | var CM var_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
    pass

def p_var(p):
    '''var : ID array'''
    if p[2] is None:
        p[0] = p[1]
    else:
        p[0] = f'{p[1]}{p[2]}'
    pass

def p_array(p):
    '''array : empty
        | SO INT SC array
    '''
    if p[1] == None:
        # Empty id_array
        p[0] = None
    else:
        # Non-empty id_array
        if p[4] is None:
            p[0] = f'[{p[2]}]'
        else:
            p[0] = f'[{p[2]}]{p[4]}' # [1][2][n]...
    pass

def p_id_array(p):
    '''id_array : SO INT SC id_array
        | SO id SC id_array
        | empty
    '''
    if len(p) == 5:
        # Non-empty id_array
        if p[4] is None:
            p[0] = f'[{p[2]}]'
        else:
            p[0] = f'[{p[2]}] {p[4]}'
    else:
        # Empty id_array
        p[0] = None
    pass

def p_id(p):
    '''id : ID
        | ID id_array
    '''
    if p[2] is not None:
        p[0] = f'{p[1]}{p[2]}'
    else:
        p[0] = f'{p[1]}'
    pass

def p_exp(p):
    '''exp : RO exp RC
        | condition
        | arigmethic
        | number_id
        | unumber_id
    '''
    if len(p) == 4:
        p[0] = p[2] # --> ( exp )
    else:
        p[0] = p[1]
    pass 

def p_condition(p):
    '''condition : NOT exp
        | exp OR exp
        | exp AND exp
        | exp MIN exp
        | exp MAJ exp
        | exp EQ EQ exp
        | exp MAJ_EQ exp
        | exp MIN_EQ exp
    '''
    if len(p) == 3:
        p[0] = f'{p[2]} {p[1]}'
    elif len(p) == 4: 
        p[0] = f'{p[3]} {p[1]} {p[2]}'
    elif len(p) == 5: 
        p[0] = f'{p[1]} {p[4]} =='
    pass

def p_arigmethic(p):
    '''arigmethic : exp PLUS exp
        | exp MINUS exp
        | exp STAR exp
        | exp DIV exp
    '''
    p[0] = f'{p[3]} {p[1]} {p[2]}'
    pass

def p_number_id(p):
    '''number_id : id 
        | INT
        | DOUBLE
    '''
    p[0] = f'{p[1]}'
    pass

def p_unumber_id(p):
    '''unumber_id : UMINUS
        | exp UMINUS
        | MINUS exp %prec UMINUS
    '''
    if len(p) == 2:
        p[0] = f'{p[1]}'
    elif p[1] == '-':
        p[0] = f'0 {p[2]} -'
    else:
        p[0] = f'{p[1]} {p[2]} +'
    pass

# def p_error(p):
#     print(f"Syntax error at line {p.lineno}, position {p.lexpos}, token {p.type}")
    # print("Syntax error somewhere")

# Build the parser
parser = ply_parser.yacc()

# Parse the source code
result = parser.parse(source_code)

# Print the parse tree
# print(result)

# print the generated assembly code
print('--------------Pseudo-assembly code----------------')
for code in assembly_code:
    print(code)