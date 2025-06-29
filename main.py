import tkinter as tk
from tkinter import messagebox, filedialog
from generator import BasicMosaicGenerator

root = tk.Tk()
root.title("Lego Mosaic Generator")
root.geometry("500x500")

# Initialize the generator
generator = BasicMosaicGenerator()

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

# Save path selection section
save_label = tk.Label(root, text="Save Output To:", font=("Arial", 12))
save_label.pack(pady=(10,5))

save_var = tk.StringVar()
save_var.set("output/lego_mosaic.png")

save_display = tk.Label(root, textvariable=save_var, font=("Arial", 10), fg="gray")
save_display.pack(pady=(0,10))

def select_save_path():
    file_path = filedialog.asksaveasfilename(
        title="Save Mosaic As",
        defaultextension=".png",
        filetypes=[
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg"),
            ("All files", "*.*")
        ]
    )
    if file_path:
        save_var.set(file_path)

save_button = tk.Button(root, text="Choose Save Location", command=select_save_path)
save_button.pack(pady=(0,20))

# Size input section
size_label = tk.Label(root, text="Mosaic Dimensions:", font=("Arial", 12))
size_label.pack(pady=(10,5))

# Width input
width_frame = tk.Frame(root)
width_frame.pack(pady=2)
width_label = tk.Label(width_frame, text="Width:", font=("Arial", 10))
width_label.pack(side=tk.LEFT, padx=(0,5))
width_var = tk.StringVar()
width_var.set("32")  # Default width
width_entry = tk.Entry(width_frame, textvariable=width_var, width=8)
width_entry.pack(side=tk.LEFT)

# Height input
height_frame = tk.Frame(root)
height_frame.pack(pady=2)
height_label = tk.Label(height_frame, text="Height:", font=("Arial", 10))
height_label.pack(side=tk.LEFT, padx=(0,5))
height_var = tk.StringVar()
height_var.set("32")  # Default height
height_entry = tk.Entry(height_frame, textvariable=height_var, width=8)
height_entry.pack(side=tk.LEFT)

def generate_mosaic():
    try:
        file_path = file_var.get()
        if file_path == "No file selected":
            messagebox.showerror("Error", "Please select an image file first.")
            return
            
        width = int(width_var.get())
        height = int(height_var.get())
        if width <= 0 or height <= 0:
            messagebox.showerror("Error", "Width and height must be positive numbers.")
            return
        
        # Get save path
        save_path = save_var.get()
        
        # Generate the mosaic
        output_path, color_info = generator.generate_mosaic(file_path, width, height, save_path)
        
        # Create info message
        info_text = f"Mosaic generated successfully!\n\nOutput: {output_path}\nSize: {width}x{height}\n\nColor usage:"
        for color, count in sorted(color_info.items(), key=lambda x: x[1], reverse=True):
            info_text += f"\n{color}: {count} bricks"
        
        messagebox.showinfo(title="Basic Mosaic Generator", message=info_text)
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to generate mosaic: {str(e)}")

generate_button = tk.Button(root, text="Generate Mosaic", command=generate_mosaic, 
                           font=("Arial", 12), bg="#4CAF50")
generate_button.pack(pady=20)

root.mainloop()
