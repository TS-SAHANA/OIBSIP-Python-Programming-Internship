import tkinter as tk
from tkinter import font, messagebox
import random
import string
import pyperclip
from PIL import Image, ImageTk

# Custom Checkbutton with styling
class StyledCheckbutton(tk.Checkbutton):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(font=font.Font(family="Helvetica", size=11, weight="bold"), fg='white', bg='dodgerblue4', activebackground='dodgerblue4', activeforeground='white', selectcolor='dodgerblue4')

        # Override the default indicator colors
        self.tk_setPalette(background='white', foreground='black', selectBackground='black', selectForeground='white')

# Main Application Class
class PasswordGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Password Generator")

        # Set window dimensions
        self.root.geometry("684x360")
        self.root.resizable(False, False)

        # Set background image
        self.bg_image = Image.open("background_image.jpg")  # Replace with your image file
        bg_photo = ImageTk.PhotoImage(self.bg_image)
        bg_label = tk.Label(root, image=bg_photo)
        bg_label.place(relwidth=1, relheight=1)

        # Variables
        self.length_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.uppercase_var = tk.BooleanVar()
        self.lowercase_var = tk.BooleanVar()
        self.digits_var = tk.BooleanVar()
        self.symbols_var = tk.BooleanVar()

        # GUI Elements
        self.create_widgets()

        # Set image as attributes to prevent garbage collection
        self.root.bg_photo = bg_photo

    # Function to create GUI widgets
    def create_widgets(self):
        # Define custom fonts
        custom_font = font.Font(family="Helvetica", size=11, weight="bold")
        button_font = font.Font(family="Helvetica", size=11, weight="bold")

        # Password Length
        self.length_label = tk.Label(self.root, text="Password Length:", fg='white', bg='black', font=custom_font)
        self.length_label.place(relx=0.05, rely=0.15, anchor="w")

        self.length_entry = tk.Entry(self.root, textvariable=self.length_var, font=custom_font)
        self.length_entry.place(relx=0.26, rely=0.15, anchor="w")

        # Character Set Options
        self.options_label = tk.Label(self.root, text="Character Set:", fg='white', bg='black', font=custom_font)
        self.options_label.place(relx=0.05, rely=0.25, anchor="w")

        # Checkboxes with custom styling
        self.uppercase_checkbox = StyledCheckbutton(self.root, text="Uppercase", variable=self.uppercase_var)
        self.uppercase_checkbox.place(relx=0.23, rely=0.25, anchor="w")

        self.lowercase_checkbox = StyledCheckbutton(self.root, text="Lowercase", variable=self.lowercase_var)
        self.lowercase_checkbox.place(relx=0.41, rely=0.25, anchor="w")

        self.digits_checkbox = StyledCheckbutton(self.root, text="Digits", variable=self.digits_var)
        self.digits_checkbox.place(relx=0.59, rely=0.25, anchor="w")

        self.symbols_checkbox = StyledCheckbutton(self.root, text="Symbols", variable=self.symbols_var)
        self.symbols_checkbox.place(relx=0.72, rely=0.25, anchor="w")

        # Generate Button with styling
        self.generate_button = tk.Button(self.root, text="Generate Password", command=self.generate_password, bg='turquoise2', activebackground='turquoise2', activeforeground='black', font=button_font)
        self.generate_button.place(relx=0.2, rely=0.4, anchor="w")

        # Generated Password
        self.password_label = tk.Label(self.root, text="Generated Password:", fg='white', bg='black', font=custom_font)
        self.password_label.place(relx=0.05, rely=0.6, anchor="w")

        self.password_entry = tk.Entry(self.root, textvariable=self.password_var, state="readonly", font=custom_font)
        self.password_entry.place(relx=0.3, rely=0.6, anchor="w")

        # Copy to Clipboard Button with styling
        self.copy_button = tk.Button(self.root, text="Copy to Clipboard", command=self.copy_to_clipboard, bg='turquoise2', activebackground='turquoise2', activeforeground='black', font=button_font)
        self.copy_button.place(relx=0.2, rely=0.75, anchor="w")

    # Function to generate a random password
    def generate_password(self):
        length_str = self.length_var.get()

        # Check if the length is empty
        if not length_str:
            messagebox.showinfo("Empty Length", "Please enter a value for password length.")
            return

        if not length_str.isdigit():
            # Show an error message if the length is not a valid integer
            messagebox.showerror("Invalid Length", "Please enter a valid numeric password length.")
            return

        length = int(length_str)
        characters = ""

        if self.uppercase_var.get():
            characters += string.ascii_uppercase
        if self.lowercase_var.get():
            characters += string.ascii_lowercase
        if self.digits_var.get():
            characters += string.digits
        if self.symbols_var.get():
            characters += string.punctuation

        if characters:
            generated_password = ''.join(random.choice(characters) for _ in range(length))
            self.password_var.set(generated_password)
        else:
            messagebox.showinfo("Character Set Error", "Select at least one character set.")

    # Function to copy the generated password to the clipboard
    def copy_to_clipboard(self):
        password = self.password_var.get()
        if password:
            pyperclip.copy(password)
            messagebox.showinfo("Password Copied", "Password copied to clipboard.")
        else:
            messagebox.showwarning("No Password", "No password to copy.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PasswordGeneratorApp(root)
    root.mainloop()