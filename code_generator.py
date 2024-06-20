
class CodeGenerator:
    def __init__(self, symbol_table, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.assembly_code = []
        self.symbol_table = symbol_table
        self.label_count = 0

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def generate(self):
        self.program()
        return "\n".join(self.assembly_code)

    def program(self):
        while self.current_token:
            self.statement()

    def statement(self):
        if self.current_token[0] == 'LCURLY':
            self.advance()
        elif self.current_token[0] == 'RCURLY':
            self.advance()
        elif self.current_token[0] == 'DATA_TYPE':
            self.declaration()
        elif self.current_token[0] == 'KEYWORD':
            if self.current_token[1] in ['iif', 'ielif', 'ielse']:
                self.conditional_statement()
            elif self.current_token[1] in ['FR', 'WH']:
                self.loop_statement()
            elif self.current_token[1] == 'Zero':
                self.function_definition()
            elif self.current_token[1] == 'cnt' or self.current_token[1] == 'br':
                self.advance()
        elif self.current_token[0] == 'FUNCTION':
            self.function_call()
            self.advance()
        elif self.current_token[0] == 'VARIABLE':
            self.assignment()
        else:
            self.advance()

    def declaration(self):
        data_type = self.current_token[1]
        self.advance()
        variable_name = self.current_token[1]
        self.advance()
        if self.current_token[0] == 'STATEMENT_END':
            self.advance()
        else:
            self.assignment(variable_name, data_type)

    def assignment(self, variable_name=None, data_type=None):
        if not variable_name:
            variable_name = self.current_token[1]
            self.advance()
        self.advance()
        value = self.expression()
        if data_type:
            if data_type == 'Num':
                self.assembly_code.append(f"MOV {variable_name}, {value}")
            elif data_type == 'Fl':
                self.assembly_code.append(f"MOV {variable_name}, {value}")
            elif data_type == 'Str':
                self.assembly_code.append(f"MOV {variable_name}, {value}")
            elif data_type == 'Bool':
                self.assembly_code.append(f"MOV {variable_name}, {1 if value == 'true' else 0}")
        else:
            self.assembly_code.append(f"MOV {variable_name}, {value}")

    def expression(self):
        left = self.term()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['+', '-']:
            operator = self.current_token[1]
            self.advance()
            right = self.term()
            temp_var = f"TMP{self.new_label()}"
            self.assembly_code.append(f"MOV {temp_var}, {left}")
            if operator == '+':
                self.assembly_code.append(f"ADD {temp_var}, {right}")
            elif operator == '-':
                self.assembly_code.append(f"SUB {temp_var}, {right}")
            left = temp_var
        return left

    def term(self):
        left = self.factor()
        while self.current_token and self.current_token[0] == 'OPERATOR' and self.current_token[1] in ['*', '/', '%']:
            operator = self.current_token[1]
            self.advance()
            right = self.factor()
            temp_var = f"TMP{self.new_label()}"
            self.assembly_code.append(f"MOV {temp_var}, {left}")
            if operator == '*':
                self.assembly_code.append(f"MUL {temp_var}, {right}")
            elif operator == '/':
                self.assembly_code.append(f"DIV {temp_var}, {right}")
            elif operator == '%':
                self.assembly_code.append(f"MOD {temp_var}, {right}")
            left = temp_var
        return left

    def factor(self):
        token = self.current_token
        token_type, token_value = token[0], token[1]
        if token_type == 'LITERAL' or token_type == 'VARIABLE' or token_type == 'CONSTANT':
            self.advance()
            return token_value
        elif token_type == 'LPAREN':
            self.advance()
            expr = self.expression()
            if self.current_token[0] == 'RPAREN':
                self.advance()
            return expr

    def condition(self):
        left_operand = self.current_token[1]
        self.advance()
        operator = self.current_token[1]
        self.advance()
        right_operand = self.current_token[1]
        self.advance()
        self.assembly_code.append(f"CMP {left_operand}, {right_operand}")
        label = self.new_label()
        if operator == '==':
            self.assembly_code.append(f"JE L{label}")
        elif operator == '!=':
            self.assembly_code.append(f"JNE L{label}")
        elif operator == '<':
            self.assembly_code.append(f"JL L{label}")
        elif operator == '>':
            self.assembly_code.append(f"JG L{label}")
        elif operator == '<=':
            self.assembly_code.append(f"JLE L{label}")
        elif operator == '>=':
            self.assembly_code.append(f"JGE L{label}")
        return label

    def conditional_statement(self):
        if self.current_token[1] == 'iif':
            self.advance()
            label = self.condition()
            self.assembly_code.append(f"JMP L{label}")
            self.assembly_code.append(f"L{label}:")
        elif self.current_token[1] == 'ielif':
            self.advance()
            label = self.condition()
            self.assembly_code.append(f"JMP L{label}")
            self.assembly_code.append(f"L{label}:")
        elif self.current_token[1] == 'ielse':
            self.advance()
            label = self.new_label()
            self.assembly_code.append(f"JMP L{label}")
            self.assembly_code.append(f"L{label}:")

    def loop_statement(self):
        if self.current_token[1] == 'FR':
            self.advance()
            self.advance()
            self.declaration()
            label = self.condition()
            self.assembly_code.append(f"JMP L{label}")
            self.assembly_code.append(f"L{label}:")
            self.advance()
            self.advance()
        elif self.current_token[1] == 'WH':
            self.advance()
            self.advance()
            label = self.condition()
            self.assembly_code.append(f"JMP L{label}")
            self.assembly_code.append(f"L{label}:")
            self.advance()
            self.advance()

    def function_call(self):
        function_name = self.current_token[1]
        self.advance()
        self.advance()
        args = []
        while self.current_token[0] != 'RPAREN':
            args.append(self.current_token[1])
            self.advance()
            if self.current_token[0] == 'SEPERATOR':
                self.advance()
        self.assembly_code.append(f"CALL {function_name} {', '.join(args)}")
        self.advance()

    def function_definition(self):
        if self.current_token[1] == 'Zero':
            self.advance()
        else:
            self.advance()
        function_name = self.current_token[1]
        self.advance()
        self.advance()
        self.assembly_code.append(f"{function_name}:")
        while self.current_token[0] != 'RPAREN':
            self.advance()
        self.advance()
        self.advance()

    def new_label(self):
        self.label_count += 1
        return f"{self.label_count}"
