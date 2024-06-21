
import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer
from main import build_symbol_table
from code_generator import CodeGenerator
from exec import AssemblyInterpreter

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AlphaLang")

        self.root.set_theme('equilux')

        mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        mainframe.place(x=0, y=0, relwidth=1, relheight=1)

        # Heading for code editor
        self.code_editor_label = ttk.Label(mainframe, text="Code", font=('Arial', 12))
        self.code_editor_label.place(x=10, y=25)

        # Text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=80, height=20, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.code_editor.place(x=10, y=50)
        self.code_editor.focus()

       # Run button with image
        image = Image.open("run_btn.png")
        image = image.resize((25, 25))
        self.run_button_image = ImageTk.PhotoImage(image)
        button_width = 20 # Width for all buttons

        self.run_button = ttk.Button(mainframe, text="Run", image=self.run_button_image, width=15,compound=tk.RIGHT, command=self.run_analysis)
        self.run_button.place(x=680, y=50)

        # Heading for results display
        self.results_display_label = ttk.Label(mainframe, text="Output", font=('Arial', 12))
        self.results_display_label.place(x=10, y=390)

        # Text widget for results
        self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=80, height=10, background='#464646', foreground='#d3d3d3', insertbackground='white',font=('Arial', 13))
        self.results_display.place(x=10, y=420)

        # Assembly Code button
        self.assembly_button = ttk.Button(mainframe, text="Assembly Code", command=self.show_assembly, width=button_width)
        self.assembly_button.place(x=680, y=100)

        # Show Tokens button
        self.tokens_button = ttk.Button(mainframe, text="Show Tokens", command=self.show_tokens, width=button_width)
        self.tokens_button.place(x=680, y=140)

        # Show Symbol Table button
        self.symbol_table_button = ttk.Button(mainframe, text="Show Symbol Table", command=self.show_symbol_table, width=button_width)
        self.symbol_table_button.place(x=680, y=180)

        # Clear Fields button
        self.clear_button = ttk.Button(mainframe, text="Clear", command=self.clear_fields, width=button_width)
        self.clear_button.place(x=680, y=220)

    def run_analysis(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        if not code:
            self.results_display.delete("1.0", tk.END)
            self.results_display.config(foreground='red')
            self.results_display.insert(tk.END, "Error: Code editor is empty. Please enter some code.")
            return

        tokens, errors = tokenize(code)
        symbol_table, symbol_table_errors = build_symbol_table(tokens)
        errors.extend(symbol_table_errors)

        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)

        semantic = SemanticAnalyzer(symbol_table, tokens)
        semantic.analyze()
        errors.extend(semantic.errors)

        self.results_display.delete("1.0", tk.END)
        if errors:
            errors = set(errors)
            self.results_display.config(foreground='red')
            for error in errors:
                self.results_display.insert(tk.END, error + '\n')
        else:
            self.results_display.config(foreground='green')
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            interpreter = AssemblyInterpreter()
            interpreter.execute(assembly_code)
            code = interpreter.debug()
            code_str = "\n".join(f"{key}: {value}" for key, value in code.items())
            self.results_display.insert(tk.END, code_str)

    def show_assembly(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table, er = build_symbol_table(tokens)

        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)

        semantic = SemanticAnalyzer(symbol_table, tokens)
        semantic.analyze()
        errors.extend(semantic.errors)
        code_generator = CodeGenerator(symbol_table, tokens)
        assembly_code = code_generator.generate()

        token_window = tk.Toplevel(self.root)
        token_window.title("Assembly Language")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, assembly_code)

    def show_tokens(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)

        tokens_str = "\n".join([f"{token}" for token in tokens])

        token_window = tk.Toplevel(self.root)
        token_window.title("Tokens")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, tokens_str)

    def update_symbol_table(self, symbol_table, interpreter_variables):
        for var_name, value in interpreter_variables.items():
            if var_name in symbol_table:
                symbol_table[var_name]['value'] = value
        return symbol_table

    def show_symbol_table(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table, symbol_table_errors = build_symbol_table(tokens)
        errors.extend(symbol_table_errors)

        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)

        semantic_analyzer = SemanticAnalyzer(symbol_table, tokens)
        semantic_analyzer.analyze()
        errors.extend(semantic_analyzer.errors)

        if errors:
            for error in errors:
                print(error)
        else:
            code_generator = CodeGenerator(symbol_table, tokens)
            assembly_code = code_generator.generate()
            interpreter = AssemblyInterpreter()
            interpreter.execute(assembly_code)
            symbol_table = self.update_symbol_table(symbol_table, interpreter.debug())
            symbol_table_window = tk.Toplevel(self.root)
            symbol_table_window.title("Symbol Table")
            columns = ('Lexeme', 'Token Type', 'Data Type', 'Line Number', 'Value')
            tree = ttk.Treeview(symbol_table_window, columns=columns, show='headings')
            for col in columns:
                tree.heading(col, text=col)
                tree.column(col, anchor='center', width=100)

            for lexeme, info in symbol_table.items():
                tree.insert('', tk.END, values=(lexeme, info['token_type'], info['data_type'], info['line_number'], info['value']))

            tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    def clear_fields(self):
        self.code_editor.delete("1.0", tk.END)
        self.results_display.delete("1.0", tk.END)
        self.results_display.config(foreground='#d3d3d3')


if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = CodeAnalyzerApp(root)
    root.geometry("850x700")  # Set a default window size
    root.mainloop()
