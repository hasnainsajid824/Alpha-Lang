class SemanticAnalyzer:
    def __init__(self, symbol_table, tokens):
        self.symbol_table = symbol_table
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.errors = []

    def analyze(self):
        self.check_variable_usage()
        self.check_function_calls()
        self.check_data_type()

        # if self.errors:
        #     print("\n\nSemantic Errors")
        #     for error in self.errors:
        #         print(error)
        # else:
        #     print("No semantic errors were found.")

    def check_variable_usage(self):
        for token_type, lexeme, line_number, *data_type in self.tokens:
            if token_type == 'VARIABLE' and lexeme not in self.symbol_table:
                self.errors.append(f"Semantic error: Variable '{lexeme}' used without declaration at line {line_number}")

    def check_function_calls(self):
        for token_type, lexeme, line_number, *data_type in self.tokens:
            if token_type == 'FUNCTION' and lexeme not in self.symbol_table:
                self.errors.append(f"Semantic error: Function '{lexeme}' called without definition at line {line_number}")

    def check_data_type(self):
        for lexeme, info in self.symbol_table.items():
            if info['token_type'] == 'VARIABLE' and info['data_type'] != None and info['value'] != None:
                if info['data_type'] == 'Num':
                    if isinstance(int(info['value']), int):
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'Fl':
                    if isinstance(float(info['value']), float):
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'Str':
                    if isinstance(info['value'], str):
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")
                elif info['data_type'] == 'Bool':
                    if info['value'] in ['true', 'false']:
                        continue
                    else:
                        self.errors.append(f"Semantic error: Variable '{lexeme}' is of type {info['data_type']} but not assigned correctly at line {info['line_number']}")

    