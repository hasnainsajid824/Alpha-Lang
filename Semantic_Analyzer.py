class SemanticAnalyzer:
    def __init__(self, symbol_table, tokens):
        self.symbol_table = symbol_table
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.errors = []

    def analyze(self):
        print('chek')
        self.check_variable_usage()
        self.check_function_calls()
        self.check_function_definitions()

        if self.errors:
            print("Semantic errors:")
            for error in self.errors:
                print(error)
        else:
            print("No semantic errors were found.")

    def check_variable_usage(self):
        for token_type, lexeme, line_number, *data_type in self.tokens:
            if token_type == 'VARIABLE' and lexeme not in self.symbol_table:
                self.errors.append(f"Semantic error: Variable '{lexeme}' used without declaration at line {line_number}")

    def check_function_calls(self):
        for token_type, lexeme, line_number, *data_type in self.tokens:
            if token_type == 'FUNCTION' and lexeme not in self.symbol_table:
                self.errors.append(f"Semantic error: Function '{lexeme}' called without definition at line {line_number}")

    def check_function_definitions(self):
        for lexeme, info in self.symbol_table.items():
            if info['token_type'] == 'FUNCTION' and info['value'] is None:
                self.errors.append(f"Semantic error: Function '{lexeme}' declared but not defined at line {info['line_number']}")
