import re

# Regular expressions for tokens
token_patterns = [
    ('NUM', r'\bNum\b'),
    ('FL', r'\bFl\b'),
    ('STR', r'\bStr\b'),
    ('BOOL', r'\bBool\b'),
    ('CHAR', r'\bChar\b'),
    ('IIF', r'\biif\b'),
    ('IELIF', r'\bielif\b'),
    ('IELSE', r'\bielse\b'),
    ('FR', r'\bFR\b'),
    ('WH', r'\bWH\b'),
    ('BRK', r'\bbrk\b'),
    ('CNT', r'\bcnt\b'),
    ('ZERO', r'\bZero\b'),
    ('AT', r'@[_a-zA-Z][_a-zA-Z0-9]*'),
    ('NUM_VAL', r'\b\d+(\.\d+)?\b'),
    ('STR_VAL', r'\".*?\"'),
    ('BOOL_VAL', r'\btrue\b|\bfalse\b'),
    ('STATEMENT_END', r'\.'),
    ('COMMA', r','),
    ('LPAREN', r'\('),
    ('RPAREN', r'\)'),
    ('LCURLY', r'\{'),
    ('RCURLY', r'\}'),
    ('PLUS', r'\+'),
    ('MINUS', r'-'),
    ('MUL', r'\*'),
    ('DIV', r'/'),
    ('MOD', r'%'),
    ('ASSIGN', r'='),
    ('COMP', r'==|<=|>=|<|>'),
    ('IDENTIFIER', r'\b[a-zA-Z][_a-zA-Z0-9]*\b'),  # Identifier must start with a letter
    ('NEWLINE', r'\n'),
    ('WHITESPACE', r'\s+'),
    ('KEYWORD', r'\b(?:Num|Fl|Str|Bool|Char|iif|ielif|ielse|FR|WH|brk|cnt|Zero)\b')
]

# Join token patterns into a single regular expression
token_regex = '|'.join('(?P<{}>{})'.format(name, pattern) for name, pattern in token_patterns)

# Lexical analyzer function
def lexical_analyzer(code):
    tokens = []
    position = 0
    line_number = 1
    while position < len(code):
        match = re.match(token_regex, code[position:])
        if match:
            token_name = match.lastgroup
            token_value = match.group(token_name)
            if token_name == 'WHITESPACE' or token_name == 'NEWLINE':
                if token_name == 'NEWLINE':
                    line_number += 1
            else:
                tokens.append((token_name, token_value, line_number))
            position += len(token_value)
        else:
            raise ValueError("Invalid token at position {}".format(position))
    return tokens

# Symbol Table class
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, datatype, line):
        if name in self.symbols:
            raise ValueError("Symbol {} already defined".format(name))
        print("Adding symbol:", name, datatype, "at line:", line)
        self.symbols[name] = (datatype, line)

    def get_datatype(self, name):
        return self.symbols.get(name, None)

def syntax_analysis(tokens):
    symbol_table = SymbolTable()
    position = 0
    while position < len(tokens):
        token = tokens[position]
        if token[0] == 'KEYWORD':
            keyword = token[1]
            if keyword in ['Num', 'Fl', 'Str', 'Bool', 'Char']:
                position += 1
                if position < len(tokens) and tokens[position][0] == 'IDENTIFIER':
                    identifier = tokens[position][1]
                    line_number = tokens[position][2]
                    symbol_table.add_symbol(identifier, keyword, line_number)
                    position += 1
                    # Skip until the next statement end
                    while position < len(tokens) and tokens[position][0] != 'STATEMENT_END':
                        position += 1
                else:
                    raise SyntaxError("Expected identifier after datatype declaration")
            else:
                raise SyntaxError("Unknown keyword: {}".format(keyword))
        position += 1  # Move to the next token
    return symbol_table

# Test the lexical analyzer and syntax analysis
if __name__ == '__main__':
    code = """
    Num @num_var = 10.
    Fl @float_var = 3.14.
    Str @string_var = "Hello, world!".
    Bool @bool_var = true.

    Num @n = 10.
    Str @message = "".
    iif @n < 10{
       @message = "Number is less than 10".
    }
    ielif @n > 10{
       @message = "Number is greater than 10".
    }
    ielse {
       @message = "Number is 10".
    }.

    FR (Num @i = 0. @i < 10. @i ++)
    { 
       @num_var = @num_var + @i.
    }.

    WH (@float_var < 10) 
    { 
       @float_var = @float_var + 1.
       cnt.
    }.

    Zero @sum (Num @n1, Num @n2)
    {
       Num @res = @n1 + @n2.
    }.

    Num @result = @sum(5, 7).

    .
    """
    try:
        tokens = lexical_analyzer(code)
        symbol_table = syntax_analysis(tokens)
        print("\nSymbol Table:")
        for symbol, (datatype, line) in symbol_table.symbols.items():
            print("{}: {} (Line {})".format(symbol, datatype, line))

    except ValueError as e:
        print(e)
    except SyntaxError as e:
        print(e)
