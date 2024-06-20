class AssemblyInterpreter:
    def __init__(self):
        self.variables = {}
        self.labels = {}
        self.program_counter = 0
        self.stack = []

    def execute(self, code):
        instructions = code.split('\n')
        self._preprocess_labels(instructions)
        while self.program_counter < len(instructions):
            instruction = instructions[self.program_counter].strip()
            if instruction:
                # print(f"Executing: {instruction}")  # Debug print for each instruction
                self._execute_instruction(instruction)
            self.program_counter += 1

    def _preprocess_labels(self, instructions):
        for idx, instruction in enumerate(instructions):
            if instruction.endswith(':'):
                label = instruction.rstrip(':')
                self.labels[label] = idx

    def _execute_instruction(self, instruction):
        parts = instruction.split()
        if parts[0].endswith(':'):
            # Skip label definitions
            return
        if parts[0] == 'MOV':
            self._execute_mov(parts[1:])
        elif parts[0] == 'ADD':
            self._execute_add(parts[1:])
        elif parts[0] == 'SUB':
            self._execute_sub(parts[1:])
        elif parts[0] == 'MUL':
            self._execute_mul(parts[1:])
        elif parts[0] == 'DIV':
            self._execute_div(parts[1:])
        elif parts[0] == 'CMP':
            self._execute_cmp(parts[1:])
        elif parts[0] in ['JL', 'JG', 'JE', 'JNE', 'JMP']:
            self._execute_jump(parts[0], parts[1] if len(parts) > 1 else None)
        elif parts[0] == 'CALL':
            self._execute_call(parts[1:])
        else:
            raise ValueError(f"Unknown instruction: {instruction}")

    def _execute_mov(self, parts):
        dest, src = parts[0], ' '.join(parts[1:])
        if src.isdigit() or (src[0] == '"' and src[-1] == '"'):
            self.variables[dest.rstrip(',')] = eval(src)  # Evaluate immediate values
        else:
            self.variables[dest.rstrip(',')] = self._evaluate_expression(src)

    def _execute_add(self, parts):
        dest, src = parts[0], parts[1]
        self.variables[dest.rstrip(',')] += self._get_value(src)

    def _execute_sub(self, parts):
        dest, src = parts[0], parts[1]
        self.variables[dest.rstrip(',')] -= self._get_value(src)

    def _execute_mul(self, parts):
        dest, src = parts[0], parts[1]
        self.variables[dest.rstrip(',')] *= self._get_value(src)

    def _execute_div(self, parts):
        dest, src = parts[0], parts[1]
        self.variables[dest.rstrip(',')] //= self._get_value(src)

    def _execute_cmp(self, parts):
        left, right = parts[0], parts[1]
        self.stack.append(('CMP', left, right))

    def _execute_jump(self, jump_type, label):
        if label is None:
            raise ValueError(f"Missing label for jump instruction: {jump_type}")
           

        if jump_type == 'JMP':
            self.program_counter = self.labels[label] - 1
        else:
            cmp_op, left, right = self.stack.pop()
            left_val = self._get_value(left)
            right_val = self._get_value(right)
            jump = False
            if jump_type == 'JL' and left_val < right_val:
                jump = True
            elif jump_type == 'JG' and left_val > right_val:
                jump = True
            elif jump_type == 'JE' and left_val == right_val:
                jump = True
            elif jump_type == 'JNE' and left_val != right_val:
                jump = True
            if jump:
                self.program_counter = self.labels[label] - 1

    def _execute_call(self, parts):
        function_name, args = parts[0], parts[1:]
        if function_name == 'print':
            for arg in args:
                print(self.variables.get(arg.rstrip(','), arg.rstrip(',')), end=' ')
            print()

    def _evaluate_expression(self, expr):
        tokens = expr.split()
        result = self._get_value(tokens[0])
        index = 1
        while index < len(tokens):
            operator = tokens[index]
            operand = tokens[index + 1]
            if operator == '+':
                result += self._get_value(operand)
            elif operator == '-':
                result -= self._get_value(operand)
            elif operator == '*':
                result *= self._get_value(operand)
            elif operator == '/':
                result //= self._get_value(operand)  # Integer division
            index += 2
        return result

    def _get_value(self, operand):
        if operand.isdigit():
            return int(operand)
        try:
            return float(operand)
        except ValueError:
            pass

        if operand.startswith('"') and operand.endswith('"'):
            return operand.strip('"')

        return self.variables.get(operand.rstrip(','), 0)

    def debug(self):
        filtered_vars = {key: value for key, value in self.variables.items() if not key.startswith('TMP')}
        print(filtered_vars)
        return filtered_vars


# code = """
# MOV @num_var, 10
# MOV @float_var, 3.14
# MOV @string_var, "Hello, world!"
# MOV @bool_var, 1
# MOV @n, 10
# MOV @message, ""
# CMP @n, 10
# JL L1
# JMP L1
# L1:
# MOV @message, "Number is less than 10"
# CMP @n, 10
# JG L2
# JMP L2
# L2:
# MOV @message, "Number is greater than 10"
# JMP L3
# L3:
# MOV @message, "Number is 10"
# MOV @i, 0
# CMP @i, 10
# JL L4
# L4:
# MOV TMPL4, @num_var
# ADD TMPL4, @i
# MOV @num_var, TMPL4
# CMP @float_var, 10
# JL L5
# L5:
# MOV TMPL5, 1
# ADD TMPL5, 2
# MOV @float_var, TMPL5
# @sum:
# MOV TMPL6, @n1
# ADD TMPL6, @n2
# MOV @res, TMPL6
# @sub:
# MOV @res, @n2
# """

# interpreter = AssemblyInterpreter()
# interpreter.execute(code)
# interpreter.debug()
