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
    quality = int(quality_entry.get())
    max_width = int(width_entry.get())
    max_height = int(height_entry.get())

    if not os.path.exists(input_file):
        messagebox.showerror("Error", "Invalid input file.")
        return

    try:
        convert_to_my_format(input_file, output_file, quality, max_width, max_height)
        messagebox.showinfo("Success", f"File converted: {output_file}")
    except Exception as e:
        messagebox.showerror("Error", f"Conversion failed: {str(e)}")

app = tk.Tk()
app.title("VIC Converter")

tk.Label(app, text="Input file:").grid(row=0, column=0, padx=5, pady=5)
input_entry = tk.Entry(app, width=40)
input_entry.grid(row=0, column=1, padx=5, pady=5)
tk.Button(app, text="Browse", command=open_file).grid(row=0, column=2, padx=5, pady=5)

tk.Label(app, text="Output file:").grid(row=1, column=0, padx=5, pady=5)
output_entry = tk.Entry(app, width=40)
output_entry.grid(row=1, column=1, padx=5, pady=5)
tk.Button(app, text="Save", command=save_file).grid(row=1, column=2, padx=5, pady=5)

tk.Label(app, text="Quality:").grid(row=2, column=0, padx=5, pady=5)
quality_entry = tk.Entry(app, width=10)
quality_entry.insert(0, "75")
quality_entry.grid(row=2, column=1, padx=5, pady=5)

tk.Label(app, text="Max width:").grid(row=3, column=0, padx=5, pady=5)
width_entry = tk.Entry(app, width=10)
width_entry.insert(0, "2000")
width_entry.grid(row=3, column=1, padx=5, pady=5)

tk.Label(app, text="Max height:").grid(row=4, column=0, padx=5, pady=5)
height_entry = tk.Entry(app, width=10)
height_entry.insert(0, "2000")
height_entry.grid(row=4, column=1, padx=5, pady=5)

tk.Button(app, text="Convert", command=convert).grid(row=5, column=0, columnspan=3, pady=10)

app.mainloop()
