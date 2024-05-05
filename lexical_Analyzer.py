import re
from Syntax_Analyzer import Parser
import sys

# Define token types
token_types = {
    'KEYWORD': r'\b(?:iif|ielif|ielse|FR|WH|Zero|cnt|br)\b',
    'DATA_TYPE': r'\b(?:Num|Fl|Str|Bool|Char)\b',
    'OPERATOR': r'(?:<=|>=|==|!=|\+\+|\-\-|\+|\-|\*|/|<|>)',
    'Identifier': r'@[_a-zA-Z][_a-zA-Z0-9]*',
    'PROCEDURE': r'\b(?:FR|WH)\b',
    'CONSTANT': r'(?:\".*?\"|\'.*?\')',
    'LITERAL': r'\b(?:true|false|\d+\.\d*|\d+)\b',
    'ASSIGN': r'=',
    'LCURLY': r'{',
    'RCURLY': r'}',
    'LPAREN': r'\(',
    'RPAREN': r'\)',
    'SEPERATOR': r'\,',
    'STATEMENT_END': r'\.',
}


# Create regular expressions for tokenization
patterns = {token: re.compile(pattern) for token, pattern in token_types.items()}

def tokenize(code):
    tokens = []
    lines = code.split('\n')
    for line_number, line in enumerate(lines, start=1):
        position = 0
        while position < len(line):
            if line[position].isspace():  # Skip whitespace
                position += 1
                continue
            match = None
            for token_type, pattern in token_types.items():
                match = re.match(pattern, line[position:])
                if match:
                    token = match.group(0)
                    if token_type == 'Identifier':
                        prev_token_index = len(tokens) - 1
                        if prev_token_index >= 0 and tokens[prev_token_index][0] == 'DATA_TYPE':
                            data_type = tokens[prev_token_index][1] if tokens[prev_token_index][0] else None
                        while position + len(token) < len(line) and  line[position + len(token)].isspace():
                                position += 1
                        if position + len(token) < len(line) and line[position + len(token)] == '(':
                            tokens.append(('FUNCTION', token, line_number, data_type))
                        else:
                            tokens.append(('VARIABLE', token, line_number, data_type))
                    else:
                        tokens.append((token_type, token, line_number))
                    position += len(token)
                    break
            if not match:
                print(f"Lexical error: Unexpected character '{line[position]}' on line {line_number}")
                position += 1
                sys.exit()

        # tokens.append('END')
    return tokens


# Function to build the symbol table
def build_symbol_table(tokens):
    symbol_table = {}
    current_data_type = None
    current_name = None
    for token_type, lexeme, line_number, *data_type in tokens:
        
        current_data_type = data_type[0] if data_type else None
        if token_type == 'VARIABLE':
            current_name = lexeme
            if current_name in symbol_table:
                # print(f"Error: Duplicate variable name '{current_name}' on line {line_number}")
                continue
            symbol_table[current_name] = {
                'token_type': 'VARIABLE',
                'data_type': current_data_type,
                'line_number': line_number,
                'value': None  # Default value for now, you can set it later
            }
        elif token_type == 'LITERAL':
            if current_name is None:
                # print(f"Error: Literal '{lexeme}' found without a preceding variable declaration on line {line_number}")
                continue
            symbol_table[current_name]['value'] = lexeme
            current_name = None  # Reset current_name after assigning value
        elif token_type == 'FUNCTION':
            current_name = lexeme
            if current_name in symbol_table:
                # print(f"Error: Duplicate function name '{current_name}' on line {line_number}")
                continue
            data_type = data_type[0] if data_type else None
            symbol_table[current_name] = {
                'token_type': 'FUNCTION',
                'data_type': data_type,
                'line_number': line_number,
                'value': None  # Default value for now, you can set it later
            }
    return symbol_table


# Read code from a file
def read_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code



code = read_code_from_file('code.txt')

# Tokenize the code
tokens = tokenize(code)

# print("Tokens:-")
# for i in tokens:
#     print(i)

# Build the symbol table
symbol_table = build_symbol_table(tokens)


# print("Symbol Table:")
# for lexeme, info in symbol_table.items():
#     print(f"{lexeme}: {info}")

# Instantiate the parser with the list of tokens
parser = Parser(tokens)
print('\nParsing ....\n')
# Parse the code
parser.parse()

