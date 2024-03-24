# AlphaLang

AlphaLang is a simple programming language designed using python. It offers a concise syntax and powerful features to make programming more efficient and enjoyable.

## Features

- **Variables**: Declare and initialize variables easily with the `@` symbol followed by alphanumeric characters and underscores.
- **Datatypes**: Supports numeric, float, string, boolean, and character datatypes.
- **Conditional Statements**: Includes `iif`, `ielif`, and `ielse` for conditional statements.
- **Iterative Statements**: Provides `FR` and `WH` loops with `brk` and `cnt` keywords for breaking and continuing loops.
- **Functions**: Define functions with return types and parameters, supporting recursion.
- **Error Handling**: Generates lexical-level errors for better code validation.


Example code:
```
Num @num_var = 10.
Str @message = "".
iif @num_var < 10 {
    @message = "Number is less than 10".
}.

print(@message).
