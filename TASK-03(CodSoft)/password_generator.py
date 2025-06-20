#### Task-03 ####

import tkinter as tk
from tkinter import messagebox, filedialog
import random
import string
from PIL import Image, ImageTk

# Function to calculate password strength
def calculate_strength(password):
    length = len(password)
    criteria = sum([
        any(c.islower() for c in password),
        any(c.isupper() for c in password),
        any(c.isdigit() for c in password),
        any(c in string.punctuation for c in password),
    ])
    
    if length >= 12 and criteria == 4:
        return "Strong", "green"
    elif length >= 8 and criteria >= 3:
        return "Medium", "orange"
    else:
        return "Weak", "red"

# Generate Password
def generate_password():
    try:
        length = int(length_entry.get())
        if length <= 0:
            raise ValueError
        
        char_pool = ''
        if var_uppercase.get():
            char_pool += string.ascii_uppercase
        if var_lowercase.get():
            char_pool += string.ascii_lowercase
        if var_digits.get():
            char_pool += string.digits
        if var_special.get():
            char_pool += string.punctuation
        
        exclude = exclude_entry.get()
        char_pool = ''.join(c for c in char_pool if c not in exclude)

        if not char_pool:
            messagebox.showwarning("Selection Error", "Please select at least one character type and ensure exclusions don’t remove all characters.")
            return
        
        password = ''.join(random.choice(char_pool) for _ in range(length))
        password_display.delete(0, tk.END)
        password_display.insert(0, password)
        update_strength(password)
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid positive integer for length.")

# Copy to Clipboard
def copy_to_clipboard():
    root.clipboard_clear()
    root.clipboard_append(password_display.get())
    messagebox.showinfo("Copied", "Password copied to clipboard!")

# Toggle Password Visibility
def toggle_password_visibility():
    if show_password_var.get():
        password_display.config(show="")
    else:
        password_display.config(show="*")

# Save to File
def save_password():
    password = password_display.get()
    label = label_entry.get().strip()
    if not password:
        messagebox.showwarning("Empty", "Generate a password first.")
        return
    if not label:
        label = "Unnamed"
    filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if filepath:
        with open(filepath, 'a') as f:
            f.write(f"{label}: {password}\n")
        messagebox.showinfo("Saved", f"Password saved under '{label}'.")

# Update strength display
def update_strength(password):
    strength, color = calculate_strength(password)
    strength_label.config(text=f"Strength: {strength}", fg=color)

# Main Window
root = tk.Tk()
root.title("Password Generator")
root.geometry("500x500")
root.resizable(False, False)
root.configure(bg="#f0f0f0")

# Load and place background image
bg_image = Image.open("background.jpg")  # 🔁 Replace with your actual image file
bg_image = bg_image.resize((500, 500), Image.Resampling.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)


# UI Elements
tk.Label(root, text="Password Generator", font=("Helvetica", 16, "bold"), bg="#f0f0f0").pack(pady=10)

tk.Label(root, text="Password Length:", bg="#f0f0f0").pack()
length_entry = tk.Entry(root, width=10, justify="center")
length_entry.pack(pady=5)

tk.Label(root, text="Exclude Characters (e.g., 0OIl):", bg="#f0f0f0").pack()
exclude_entry = tk.Entry(root, width=30, justify="center")
exclude_entry.pack(pady=5)

var_uppercase = tk.BooleanVar(value=True)
var_lowercase = tk.BooleanVar(value=True)
var_digits = tk.BooleanVar(value=True)
var_special = tk.BooleanVar(value=True)

tk.Checkbutton(root, text="Include Uppercase (A-Z)", variable=var_uppercase, bg="#f0f0f0").pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Include Lowercase (a-z)", variable=var_lowercase, bg="#f0f0f0").pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Include Digits (0-9)", variable=var_digits, bg="#f0f0f0").pack(anchor="w", padx=50)
tk.Checkbutton(root, text="Include Special (!@#...)", variable=var_special, bg="#f0f0f0").pack(anchor="w", padx=50)

tk.Button(root, text="Generate Password", command=generate_password, bg="#4CAF50", fg="white").pack(pady=10)

# Show/hide password
show_password_var = tk.BooleanVar()
tk.Checkbutton(root, text="Show Password", variable=show_password_var, command=toggle_password_visibility, bg="#f0f0f0").pack()

# Password entry
password_display = tk.Entry(root, font=("Courier", 12), justify="center", width=30, show="*")
password_display.pack(pady=5)

# Strength indicator
strength_label = tk.Label(root, text="Strength: ", font=("Helvetica", 10, "bold"), bg="#f0f0f0")
strength_label.pack()

# Copy and save buttons
tk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, bg="#2196F3", fg="white").pack(pady=5)

tk.Label(root, text="Label (e.g., Gmail, Facebook):", bg="#f0f0f0").pack()
label_entry = tk.Entry(root, width=30, justify="center")
label_entry.pack(pady=5)
tk.Button(root, text="Save to File", command=save_password, bg="#9C27B0", fg="white").pack(pady=5)

for widget in root.winfo_children():
    widget.lift()


root.mainloop()
