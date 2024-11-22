# PLY Lexer and Parser

This project implements a lexer (scanner) and a parser using the [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/) library. The program processes a custom language and generates pseudo-assembly code as output.

## Features

- **Lexical Analysis**: Tokenizes the input source code into a set of tokens using defined regular expressions.
- **Syntax Analysis**: Parses the tokens to validate their structure against the grammar rules defined.
- **Pseudo-Assembly Code Generation**: Converts the parsed code into a pseudo-assembly representation.
- **Error Handling**: Identifies and reports syntax and semantic errors in the source code.

## Requirements

- Python 3.7 or higher
- [PLY (Python Lex-Yacc)](https://www.dabeaz.com/ply/)

To install PLY, use:

```bash
pip install ply
