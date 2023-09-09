# import ply lexer
from ply import lex

# Declaration of the assigned tokens
# for lexer from ply to use when scanning the code
assigned_tokens = [
    'VAR',
    'INT',
    'DOUBLE',
    'COMMENT',
    'WHITESPACE'
]

# Continue lex
