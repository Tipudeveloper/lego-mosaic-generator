import tkinter as tk

root = tk.Tk()
root.title("lego mosaic generator")
root.geometry("300x200")

label = tk.Label(root, text="lego mosaic generator", font=("Arial", 14))
label.pack(pady=20)

def press():
    print("but nothing happened")

button = tk.Button(root, text="generate mosaic", command=press)
button.pack()

root.mainloop()
