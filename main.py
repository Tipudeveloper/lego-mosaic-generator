import tkinter as tk
from tkinter import messagebox, filedialog

root = tk.Tk()
root.title("Lego Mosaic Generator")
root.geometry("500x400")

label = tk.Label(root, text="Lego Mosaic Generator", font=("Arial", 14))
label.pack(pady=20)

# File selection section
file_label = tk.Label(root, text="Select Image File:", font=("Arial", 12))
file_label.pack(pady=(10,5))

file_var = tk.StringVar()
file_var.set("No file selected")

file_display = tk.Label(root, textvariable=file_var, font=("Arial", 10), fg="gray")
file_display.pack(pady=(0,10))

def select_file():
    file_path = filedialog.askopenfilename(
        title="Select Image File",
        filetypes=[
            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("All files", "*.*")
        ]
    )
    if file_path:
        file_var.set(file_path)

file_button = tk.Button(root, text="Browse Files", command=select_file)
file_button.pack(pady=(0,20))

# Size input section
size_label = tk.Label(root, text="Mosaic Size:", font=("Arial", 12))
size_label.pack(pady=(10,5))

size_var = tk.StringVar()
size_var.set("32")  # Default size
size_entry = tk.Entry(root, textvariable=size_var, width=10)
size_entry.pack()

def generate_mosaic():
    try:
        file_path = file_var.get()
        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select an image file first.")
            return
            
        size = int(size_var.get())
        if size <= 0:
            messagebox.showerror("Error", "Size must be a positive number.")
            return
            
        messagebox.showinfo(title="Lego Mosaic Generator", 
                          message=f"Generating mosaic from: {file_path}\nSize: {size}x{size}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number for size.")

generate_button = tk.Button(root, text="Generate Mosaic", command=generate_mosaic, 
                           font=("Arial", 12), bg="#4CAF50")
generate_button.pack(pady=20)

root.mainloop()
