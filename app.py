import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from ttkthemes import ThemedTk
from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer
from main import build_symbol_table


class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Analyzer")

        # Apply the Equilux theme
        self.root.set_theme('equilux')

        # Create a frame for better layout management
        mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Heading for code editor
        self.code_editor_label = ttk.Label(mainframe, text="Code Editor")
        self.code_editor_label.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        # Text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.code_editor.grid(row=1, column=0, padx=10, pady=5)

        # Heading for results display
        self.results_display_label = ttk.Label(mainframe, text="Output")
        self.results_display_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        # Text widget for results
        self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        self.results_display.grid(row=1, column=1, padx=10, pady=5)

        # Run button
        self.run_button = ttk.Button(mainframe, text="Run", style='Run.TButton', command=self.run_analysis)
        self.run_button.grid(row=2, column=0, padx=10, pady=10, sticky='w')

        # Show Tokens button
        self.tokens_button = ttk.Button(mainframe, text="Show Tokens", command=self.show_tokens,)
        self.tokens_button.grid(row=2, column=1, padx=5, pady=10, sticky='w')

        # Show Symbol Table button
        self.symbol_table_button = ttk.Button(mainframe, text="Show Symbol Table", command=self.show_symbol_table,)
        self.symbol_table_button.grid(row=2, column=1, padx=10, pady=10, sticky='e')

    def run_analysis(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table = build_symbol_table(tokens)
        
        parser = Parser(tokens)
        parser.parse()
        errors.extend(parser.errors)
        
        semantic = SemanticAnalyzer(symbol_table, tokens)
        semantic.analyze()
        errors.extend(semantic.errors)

        self.results_display.delete("1.0", tk.END)
        if errors:
            self.results_display.config(foreground='red')
            for error in errors:
                self.results_display.insert(tk.END, error + '\n')
        else:
            self.results_display.config(foreground='green')
            self.results_display.insert(tk.END, 'No Errors were found\n')

    def show_tokens(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)

        tokens_str = "\n".join([f"{token}" for token in tokens])

        token_window = tk.Toplevel(self.root)
        token_window.title("Tokens")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30, background='#464646', foreground='#d3d3d3', insertbackground='white')
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, tokens_str)

    def show_symbol_table(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table = build_symbol_table(tokens)

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

if __name__ == "__main__":
    root = ThemedTk(theme="equilux")
    app = CodeAnalyzerApp(root)
    root.mainloop()