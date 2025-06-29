import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Lego Mosaic Generator")
root.geometry("300x200")

label = tk.Label(root, text="Lego Mosaic Generator", font=("Arial", 14))
label.pack(pady=20)

value_var = tk.StringVar()
value_entry = tk.Entry(root, textvariable=value_var)
value_entry.pack()

def loop():
    try:
        value = int(value_var.get())
    except ValueError:
        pass
    root.after(500, loop)

loop()


def press():
    try:
        value = int(value_var.get())
        messagebox.showinfo(title="lego mosaic generator", message=f"Generating value: {value}")
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid number.")

button = tk.Button(root, text="Generate Mosaic", command=press)
button.pack()

root.mainloop()
