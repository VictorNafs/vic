import tkinter as tk
from tkinter import filedialog, messagebox
import os
from convert_to_my_format import convert_to_my_format

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("PNG Files", "*.png")])
    input_entry.delete(0, tk.END)
    input_entry.insert(0, file_path)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".vic", filetypes=[("VIC Files", "*.vic")])
    output_entry.delete(0, tk.END)
    output_entry.insert(0, file_path)

def convert():
    input_file = input_entry.get()
    output_file = output_entry.get()

    if not os.path.exists(input_file):
        messagebox.showerror("Error", "Invalid input file.")
        return

    try:
        # Appel de la fonction convert_to_my_format avec qualité par défaut
        convert_to_my_format(input_file, output_file)
        messagebox.showinfo("Success", f"File converted successfully: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {str(e)}")

# Configuration de l'interface graphique
app = tk.Tk()
app.title("VIC Converter")

# Fichier d'entrée
tk.Label(app, text="Input file:").grid(row=0, column=0, padx=5, pady=5)
input_entry = tk.Entry(app, width=40)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(app, text="Browse", command=open_file).grid(row=0, column=2, padx=5, pady=5)

# Fichier de sortie
tk.Label(app, text="Output file:").grid(row=1, column=0, padx=5, pady=5)
output_entry = tk.Entry(app, width=40)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(app, text="Save", command=save_file).grid(row=1, column=2, padx=5, pady=5)

# Bouton Convert
tk.Button(app, text="Convert", command=convert).grid(row=2, column=0, columnspan=3, pady=10)

# Lancer l'application
app.mainloop()
