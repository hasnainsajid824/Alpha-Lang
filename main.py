import re
from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer
from code_generator import CodeGenerator
Errors = []

# Function to build the symbol table
def build_symbol_table(tokens):
    symbol_table = {}
    current_data_type = None
    current_name = None
    error = []
    for token_type, lexeme, line_number, *data_type in tokens:
        
        current_data_type = data_type[0] if data_type else None
        if token_type == 'VARIABLE':
            current_name = lexeme
            if current_data_type == None:
                current_name = None
                continue
            symbol_table[current_name] = {
                'token_type': 'VARIABLE',
                'data_type': current_data_type,
                'line_number': line_number,
                'value': None  
            }
        elif token_type == 'LITERAL' or token_type == 'CONSTANT':
            if current_name is None:
                continue
            
            if symbol_table[current_name]['token_type'] == 'VARIABLE' or current_name in symbol_table:
                symbol_table[current_name]['value'] = lexeme
            current_name = None  # Reset current_name after assigning value
        elif token_type == 'FUNCTION':
            current_name = lexeme
            if current_name in symbol_table:
                # error.append(f"Error: Duplicate function name '{current_name}' on line {line_number}")
                continue
            data_type = data_type[0] if data_type else None
            if data_type != None:
                symbol_table[current_name] = {
                    'token_type': 'FUNCTION',
                    'data_type': data_type,
                    'line_number': line_number,
                    'value': None  
                }   

    return symbol_table, error


# Read code from a file
def read_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code



code = read_code_from_file('code.txt')


# Tokenize the code
tokens, errors = tokenize(code)
Errors.extend(errors)


# Build the symbol table
symbol_table, symbol_table_errors = build_symbol_table(tokens)
Errors.extend(symbol_table_errors)
# Parse the code
parser = Parser(tokens)
parser.parse()
Errors.extend(parser.errors)

semantic_analyzer = SemanticAnalyzer(symbol_table, tokens)
semantic_analyzer.analyze()
Errors.extend(semantic_analyzer.errors)

if Errors:
    for error in Errors:
        print(error)
else:
    code_generator = CodeGenerator(symbol_table, tokens)
    assembly_code = code_generator.generate()
    with open("output.asm", "w") as f:
        f.write(assembly_code)