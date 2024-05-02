import sys
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        self.current_token = self.tokens[self.current_token_index] if self.tokens else None
        self.block_stack = []

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            self.current_token = self.tokens[self.current_token_index]
        else:
            self.current_token = None

    def match(self, expected_token_type):
        if self.current_token and self.current_token[0] == expected_token_type or self.current_token == None:
            self.advance()
        else:
            print(f"Syntax error: Expected {expected_token_type}, found {self.current_token[0] if self.current_token else 'EOF'} at line {self.current_token[2]}")
            

    def parse(self):
        self.program()
        print('No Syntax Error were found')

    def program(self):
        self.statement_list()

    def statement_list(self):
        while self.current_token:
            self.statement()
        if self.current_token == None and len(self.block_stack) > 0:
                er = '}'
                print(f"Syntax error: Missing {er} of Block at line {self.block_stack[-1][1]}")
        

    def statement(self):
        if self.current_token[0] == 'LCURLY':
            self.block()
        elif self.current_token[0] == 'RCURLY':
            print('check', self.current_token[2])
            if self.block_stack:
                self.block_stack.pop()
                # return
            # else:
            #     print(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
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
                self.match('STATEMENT_END')
        elif self.current_token[0] == 'FUNCTION':            
            self.function_call()
        elif self.current_token[0] == 'VARIABLE':
            self.assignment()
        elif self.current_token == None:
                pass
        else:
            print(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            self.advance()
            

    def expression(self):
        if self.current_token[0] in ['LITERAL', 'CONSTANT', 'VARIABLE', 'OPERATOR']:
            self.match(self.current_token[0])
            return False
        elif self.current_token[0] == 'FUNCTION':
            self.function_call()
            return True
        else:
            print(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            #self.advance()
            return True
            
    

    def declaration(self):
        self.match('DATA_TYPE')
        if self.current_token[0] == 'FUNCTION':
                self.function_definition()
        else:
            self.match('VARIABLE')
            self.match('ASSIGN')
            self.expression()
            self.match('STATEMENT_END')

    def assignment(self):
        self.match('VARIABLE')
        self.match('ASSIGN')
        while self.current_token[0] != 'STATEMENT_END':
            if self.expression():
                break
        self.match('STATEMENT_END')
        
    def condition(self):
        self.expression()
        self.match('OPERATOR')
        self.expression()

    def conditional_statement(self):
        if self.current_token[1] == 'iif':
            self.match('KEYWORD')
            self.condition()
            self.block()
        elif self.current_token[1] == 'ielif':
                self.match('KEYWORD')
                self.condition()
                self.block()
        elif self.current_token[1] == 'ielse':
                self.match('KEYWORD')
                self.block()

    def loop_progression(self):
        if self.current_token[0] == 'VARIABLE':
            self.match('VARIABLE') 
            self.match('OPERATOR')
            if self.current_token[0] == 'VARIABLE':
                self.match('VARIABLE') 
        elif self.current_token[0] == 'OPERATOR':
            self.match('OPERATOR')  
            if self.current_token[0] == 'LITERAL':
                self.match('LITERAL')  
            elif self.current_token[0] == 'VARIABLE':
                self.match('VARIABLE')  
            else:
                print(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
                self.advance()
                
        else:
            print(f"Syntax error: Unexpected token {self.current_token[1]} at line {self.current_token[2]}")
            self.advance()
            

    def loop_statement(self):
        if self.current_token[1] == 'FR':
            self.match('KEYWORD')
            self.match('LPAREN')
            self.declaration()
            self.condition()
            self.match('STATEMENT_END')
            self.loop_progression()
            self.match('RPAREN')
            self.block()
        elif self.current_token[1] == 'WH':
            self.match('KEYWORD')
            self.match('LPAREN')
            self.condition()
            self.match('RPAREN')
            self.block()

    def argument_list(self):
        while self.current_token and self.current_token[0] != 'RPAREN':
            if self.current_token[0] == 'DATA_TYPE':
                self.match(self.current_token[0])
                self.match('VARIABLE')
            elif self.current_token[0] == 'VARIABLE':
                self.match(self.current_token[0])
            elif self.current_token[0] == 'SEPERATOR':
                self.match(self.current_token[0])
            self.advance()
        self.match('RPAREN')

    def function_call(self):
        self.match('FUNCTION')
        self.match('LPAREN')
        if self.current_token[0] != 'RPAREN':
            self.argument_list()
        self.match('STATEMENT_END')
    
    def function_definition(self):
        if self.current_token[1] == 'Zero':
            self.match('KEYWORD')
        else:
            self.match('DATA_TYPE')
        self.match('FUNCTION')
        self.match('LPAREN')
        if self.current_token[0] != 'RPAREN':
            self.argument_list()
        print('check', self.current_token[2]) 
        self.block()
        self.match('RCURLY')
        self.block_stack.pop()

    def block(self):
        if self.current_token == None:
            return
        self.block_stack.append(('BLOCK', self.current_token[2]))
        
        self.match('LCURLY')
        self.statement_list()
        


