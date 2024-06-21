import re

# Define token types
token_types = {
    'KEYWORD': r'\b(?:iif|ielif|ielse|FR|WH|Zero|cnt|br|null|print|input)\b',
    'DATA_TYPE': r'\b(?:Num|Fl|Str|Bool|Char)\b',
    'OPERATOR': r'(?:<=|>=|==|!=|\+\+|\-\-|\+|\-|\*|/|<|>|%)',
    'Identifier': r'@[_a-zA-Z][_a-zA-Z0-9]*',
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
    Errors = []
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
                        data_type = None  # Default to None
                        if prev_token_index >= 0 and tokens[prev_token_index][0] == 'DATA_TYPE' or tokens[prev_token_index][1] == 'Zero':
                            data_type = tokens[prev_token_index][1]
                        while position + len(token) < len(line) and line[position + len(token)].isspace():
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
                Errors.append(f"Lexical error: Unexpected character '{line[position]}' on line {line_number}")
                print(f"Lexical error: Unexpected character '{line[position]}' on line {line_number}")
                position += 1

    return tokens, Errors


