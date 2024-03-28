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
    symbol_table = SymbolTable()
    lines = code.split('\n')
    line_number = 1
    for line in lines:
        position = 0
        while position < len(line):
            match = re.match(token_regex, line[position:])
            if match:
                token_name = match.lastgroup
                token_value = match.group(token_name)
                if token_name == 'WHITESPACE' or token_name == 'NEWLINE':
                    pass  # Ignore whitespace and newline tokens
                else:
                    symbol_table.add_symbol(token_value, line_number)  # Add identifier to symbol table
                    tokens.append((token_name, token_value, line_number))
                position += len(token_value)
            else:
                raise ValueError("Invalid token at position {} in line {}".format(position, line_number))
        line_number += 1
    return tokens, symbol_table

# Symbol Table class
class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def add_symbol(self, name, line_number):
        if name not in self.symbols:
            self.symbols[name] = []
        self.symbols[name].append(line_number)

    def display(self):
        for symbol, line_numbers in self.symbols.items():
            print("{} : {}".format(symbol, line_numbers))


# Test the lexical analyzer
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
        tokens, symbol_table = lexical_analyzer(code)
        print("\nSymbol Table:")
        symbol_table.display()

    except ValueError as e:
        print(e)
