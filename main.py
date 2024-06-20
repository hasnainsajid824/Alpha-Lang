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
tokens, errors = tokenize(code)

if errors:
    for error in errors:
        print(error)
else:
    # Build the symbol table
    symbol_table = build_symbol_table(tokens)
    
    # Parse the code
    parser = Parser(tokens)
    parser.parse()
    
    if parser.errors:
        for error in parser.errors:
            print(error)
    else:
        # Semantic analysis
        semantic_analyzer = SemanticAnalyzer(symbol_table, tokens)
        semantic_analyzer.analyze()
        
        if semantic_analyzer.errors:
            for error in semantic_analyzer.errors:
                print(error)
        else:
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            with open("output.asm", "w") as f:
                f.write(assembly_code)