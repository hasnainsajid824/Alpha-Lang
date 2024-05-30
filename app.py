import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk

# Assuming your lexical_Analyzer, Syntax_Analyzer, and Semantic_Analyzer are imported
from lexical_Analyzer import tokenize
from Syntax_Analyzer import Parser
from Semantic_Analyzer import SemanticAnalyzer
from main import build_symbol_table

class CodeAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Code Analyzer")
        
        # Apply the 'clam' theme
        style = ttk.Style()
        style.theme_use('clam')
        
        # Create a frame for better layout management
        mainframe = ttk.Frame(self.root, padding="10 10 10 10")
        mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # Text widget for code editor
        self.code_editor = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30)
        self.code_editor.grid(row=0, column=0, padx=10, pady=10)

        # Text widget for results
        self.results_display = scrolledtext.ScrolledText(mainframe, wrap=tk.WORD, width=60, height=30)
        self.results_display.grid(row=0, column=1, padx=10, pady=10)

        # Run button
        self.run_button = ttk.Button(mainframe, text="Run", command=self.run_analysis)
        self.run_button.grid(row=1, column=0, padx=10, pady=10, sticky='w')

        # Show Tokens button
        self.tokens_button = ttk.Button(mainframe, text="Show Tokens", command=self.show_tokens)
        self.tokens_button.grid(row=1, column=1, padx=10, pady=10, sticky='w')

        # Show Symbol Table button
        self.symbol_table_button = ttk.Button(mainframe, text="Show Symbol Table", command=self.show_symbol_table)
        self.symbol_table_button.grid(row=1, column=1, padx=10, pady=10, sticky='e')

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
            for error in errors:
                self.results_display.insert(tk.END, error + '\n')
        else:
            self.results_display.insert(tk.END, 'No Errors were found\n')

    def show_tokens(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)

        tokens_str = "\n".join([f"{token}" for token in tokens])

        token_window = tk.Toplevel(self.root)
        token_window.title("Tokens")
        token_text = scrolledtext.ScrolledText(token_window, wrap=tk.WORD, width=80, height=30)
        token_text.pack(padx=10, pady=10)
        token_text.insert(tk.END, tokens_str)

    def show_symbol_table(self):
        code = self.code_editor.get("1.0", tk.END).strip()
        tokens, errors = tokenize(code)
        symbol_table = build_symbol_table(tokens)

        symbol_table_str = "\n".join([f"{lexeme}: {info}" for lexeme, info in symbol_table.items()])

        symbol_table_window = tk.Toplevel(self.root)
        symbol_table_window.title("Symbol Table")
        symbol_table_text = scrolledtext.ScrolledText(symbol_table_window, wrap=tk.WORD, width=80, height=30)
        symbol_table_text.pack(padx=10, pady=10)
        symbol_table_text.insert(tk.END, symbol_table_str)

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeAnalyzerApp(root)
    root.mainloop()
