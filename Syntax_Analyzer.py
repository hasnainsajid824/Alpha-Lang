def syntax_analysis(symbol_table, tokens):
    position = 0
    while position < len(tokens):
        token = tokens[position]
        token_type = token[0]
        token_value = token[1]
        token_line = token[2]

        # Handle variable declaration
        if token_type == 'DATA_TYPE':
            if position + 3 < len(tokens):
                if tokens[position + 1][0] == 'VARIABLE' and tokens[position + 2][0] == 'ASSIGN' and tokens[position + 3][0] in ['LITERAL', 'CONSTANT']:
                    position += 3  # Skip the variable declaration
                else:
                    print("Syntax Error: Invalid variable declaration syntax at line", token_line)
            else:
                print("Syntax Error: Incomplete variable declaration at line", token_line)

        # Handle if statement
        elif token_type == 'KEYWORD' and token_value == 'iif':
            # Implement logic to check if statement syntax
            # ...
            print("Syntax Error: Invalid if statement syntax at line", token_line)

        # Handle for loop
        elif token_type == 'KEYWORD' and token_value == 'FR':
            # Implement logic to check for loop syntax
            # ...
            print("Syntax Error: Invalid for loop syntax at line", token_line)

        # Handle while loop
        elif token_type == 'KEYWORD' and token_value == 'WH':
            # Implement logic to check while loop syntax
            # ...
            print("Syntax Error: Invalid while loop syntax at line", token_line)

        # Handle function definition
        elif token_type == 'KEYWORD' and token_value == 'Zero':
            if position + 4 < len(tokens):
                if tokens[position + 1][0] == 'FUNCTION' and tokens[position + 2][0] == 'VARIABLE' and tokens[position + 3][0] == 'LPAREN' and tokens[position + 4][0] == 'RPAREN':
                    position += 4  # Skip the function definition
                else:
                    print("Syntax Error: Invalid function definition syntax at line", token_line)
            else:
                print("Syntax Error: Incomplete function definition at line", token_line)

        # Handle other statements or expressions
        else:
            # Implement logic to handle other statements or expressions
            # ...
            print("Syntax Error: Invalid syntax at line", token_line)

        position += 1
