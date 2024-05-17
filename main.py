import re
from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer

Errors = []

# Function to build the symbol table
def build_symbol_table(tokens):
    symbol_table = {}
    current_data_type = None
    current_name = None
    for token_type, lexeme, line_number, *data_type in tokens:
        
        current_data_type = data_type[0] if data_type else None
        if token_type == 'VARIABLE':
            current_name = lexeme
            if current_name in symbol_table or current_data_type == None:
                current_name = None
                # print(f"Error: Duplicate variable name '{current_name}' on line {line_number}")
                continue
            symbol_table[current_name] = {
                'token_type': 'VARIABLE',
                'data_type': current_data_type,
                'line_number': line_number,
                'value': None  
            }
        elif token_type == 'LITERAL' or token_type == 'CONSTANT':
            if current_name is None:
                # print(f"Error: Literal '{lexeme}' found without a preceding variable declaration on line {line_number}")
                continue
            
            if symbol_table[current_name]['token_type'] == 'VARIABLE':
                symbol_table[current_name]['value'] = lexeme
            current_name = None  # Reset current_name after assigning value
        elif token_type == 'FUNCTION':
            current_name = lexeme
            if current_name in symbol_table:
                # print(f"Error: Duplicate function name '{current_name}' on line {line_number}")
                continue
            data_type = data_type[0] if data_type else None
            if data_type != None:
                symbol_table[current_name] = {
                    'token_type': 'FUNCTION',
                    'data_type': data_type,
                    'line_number': line_number,
                    'value': None  
                }   

    return symbol_table


# Read code from a file
def read_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code



code = read_code_from_file('code.txt')

# Tokenize the code
tokens, error = tokenize(code)

Errors.extend(error)

# print("Tokens:-")
# for i in tokens:
#     print(i)

# Build the symbol table
symbol_table = build_symbol_table(tokens)

      
# print("Symbol Table:")
# for lexeme, info in symbol_table.items():
#     print(f"{lexeme}: {info}")

parser = Parser(tokens)
# print('\nParsing ....\n')
# Parse the code
parser.parse()
Errors.extend(parser.errors)

semantic = SemanticAnalyzer(symbol_table, tokens)
semantic.analyze()
Errors.extend(semantic.errors)

if Errors:
    for i in Errors:
        print(i)
else:
    print('No Errors were found')