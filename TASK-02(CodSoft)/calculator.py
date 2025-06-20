#### Task-02 ####

import tkinter as tk
from tkinter import messagebox

class SimpleCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title(" Calculator")
        self.root.geometry("400x580")
        self.root.resizable(False, False)

        self.expression = ""
        self.dark_mode = False

        self.history = []  # Stores past calculations
        self.history_var = tk.StringVar()
        self.history_var.set("History")
        self.history_dropdown = None  # Will hold OptionMenu

        self.font = ("Times New Roman", 14)
        self.entry_font = ("Times New Roman", 21)

        self.light_bg = "#f5f5f5"
        self.dark_bg = "#2c2c2c"
        self.light_fg = "#000000"
        self.dark_fg = "#ffffff"
        self.gradient_colors = ["#edc0f4", "#ebaef4", "#e696f3", "#cbbc4d"]  # Simulated gradient

        self.create_widgets()

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        if self.history_dropdown:
            self.history_dropdown.destroy()
            self.history_dropdown = None

    def create_widgets(self):
        # Theme toggle
        top_frame = tk.Frame(self.root)
        top_frame.pack(pady=5)

        self.toggle_btn = tk.Button(top_frame, text="Toggle Theme", font=self.font, command=self.toggle_theme)
        self.toggle_btn.pack(side=tk.LEFT, padx=5)

        self.history_btn = tk.Button(top_frame, text="History ▼", font=self.font, command=self.toggle_history_dropdown)
        self.history_btn.pack(side=tk.LEFT, padx=5)

        # Entry
        self.entry = tk.Entry(self.root, font=self.entry_font, bd=10, relief=tk.RIDGE, justify='right')
        self.entry.pack(fill=tk.BOTH, ipadx=8, ipady=15, padx=10, pady=10)

        # Calculator buttons
        buttons = [
            ['C', '(', ')', '/'],
            ['7', '8', '9', '*'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['0', '.', '%', '=']
        ]

        self.button_widgets = []

        for row in buttons:
            frame = tk.Frame(self.root)
            frame.pack(expand=True, fill="both")
            row_buttons = []
            for idx, btn_text in enumerate(row):
                color = self.gradient_colors[idx % len(self.gradient_colors)]
                btn = tk.Button(frame, text=btn_text, font=self.font, bd=1, relief=tk.RAISED,
                                command=lambda char=btn_text: self.on_button_click(char),
                                bg=color)
                btn.pack(side=tk.LEFT, expand=True, fill="both")
                row_buttons.append(btn)
            self.button_widgets.append(row_buttons)

        # Initialize prompt frame (empty at start)
        self.prompt_frame = tk.Frame(self.root)
        self.prompt_frame.pack()

    def toggle_history_dropdown(self):
        if self.history_dropdown:
            self.history_dropdown.destroy()
            self.history_dropdown = None
        else:
            if not self.history:
                messagebox.showinfo("History", "No history yet.")
                return
            self.history_dropdown = tk.OptionMenu(self.root, self.history_var, *self.history)
            self.history_dropdown.config(font=self.font)
            self.history_dropdown.pack(pady=5)

            self.create_prompt()
            self.apply_theme()

    def create_prompt(self):
        for widget in self.prompt_frame.winfo_children():
            widget.destroy()

        tk.Label(self.prompt_frame, text="Num 1:", font=self.font).grid(row=0, column=0, padx=5)
        self.num1_entry = tk.Entry(self.prompt_frame, width=5, font=self.font)
        self.num1_entry.grid(row=0, column=1)

        tk.Label(self.prompt_frame, text="Operation:", font=self.font).grid(row=0, column=2, padx=5)
        self.op_entry = tk.Entry(self.prompt_frame, width=5, font=self.font)
        self.op_entry.grid(row=0, column=3)

        tk.Label(self.prompt_frame, text="Num 2:", font=self.font).grid(row=0, column=4, padx=5)
        self.num2_entry = tk.Entry(self.prompt_frame, width=5, font=self.font)
        self.num2_entry.grid(row=0, column=5)

        tk.Button(self.prompt_frame, text="Calculate", font=self.font, command=self.calculate_from_prompt).grid(row=2, column=2, columnspan=2, padx=10)

    def on_button_click(self, char):
        if char == 'C':
            self.expression = ""
            self.entry.delete(0, tk.END)
        elif char == '=':
            try:
                result = str(eval(self.expression))
                self.entry.delete(0, tk.END)
                self.entry.insert(tk.END, result)
                self.history.append(f"{self.expression} = {result}")
                self.expression = result
            except Exception:
                messagebox.showerror("Error", "Invalid Expression")
                self.entry.delete(0, tk.END)
                self.expression = ""
        else:
            self.expression += str(char)
            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, self.expression)

    def calculate_from_prompt(self):
        try:
            num1 = float(self.num1_entry.get())
            num2 = float(self.num2_entry.get())
            op = self.op_entry.get().strip()

            if op not in ['+', '-', '*', '/', '%']:
                raise ValueError("Invalid operation")

            if op == '+':
                result = num1 + num2
            elif op == '-':
                result = num1 - num2
            elif op == '*':
                result = num1 * num2
            elif op == '/':
                if num2 == 0:
                    raise ZeroDivisionError("Cannot divide by zero")
                result = num1 / num2
            elif op == '%':
                result = (num1 * num2) / 100

            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(result))
            self.expression = str(result)
            self.history.append(f"{num1} {op} {num2} = {result}")
        except ValueError:
            messagebox.showerror("Input Error", "Please enter valid numbers and operator.")
        except ZeroDivisionError as zde:
            messagebox.showerror("Math Error", str(zde))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def apply_theme(self):
        bg = self.dark_bg if self.dark_mode else self.light_bg
        fg = self.dark_fg if self.dark_mode else self.light_fg

        self.root.configure(bg=bg)
        self.entry.configure(bg=bg, fg=fg, insertbackground=fg)
        self.toggle_btn.configure(bg=bg, fg=fg, activebackground=fg, activeforeground=bg)
        self.history_btn.configure(bg=bg, fg=fg, activebackground=fg, activeforeground=bg)

        for row in self.button_widgets:
            for btn in row:
                btn.configure(fg=fg)

        for widget in self.prompt_frame.winfo_children():
            if isinstance(widget, tk.Label) or isinstance(widget, tk.Button):
                widget.configure(bg=bg, fg=fg)
            elif isinstance(widget, tk.Entry):
                widget.configure(bg="white" if not self.dark_mode else "#555555", fg=fg, insertbackground=fg)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleCalculator(root)
    root.mainloop()
