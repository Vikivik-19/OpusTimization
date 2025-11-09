import tkinter as tk
from tkinter import messagebox
import subprocess

# Function when the "Continue" button is clicked
def continue_action():
    try:
        # Execute the main.py script
        subprocess.run(['python', 'main.py'], check=True)
        messagebox.showinfo("Next Step", "You can now proceed with the next steps!")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while running main.py: {e}")

# Create the main window
root = tk.Tk()
root.title("OPUS Optimal Combination")
root.geometry("800x600")
root.config(bg="#E0F2F1")  # Light blue background

# Set a font style for labels and buttons
font_style = ('Helvetica', 12)
bold_font = ('Helvetica', 14, 'bold')

# Header
header_frame = tk.Frame(root, bg="#00AEEF", padx=30, pady=20)
header_frame.pack(fill="x")

# Main heading
main_heading = tk.Label(header_frame, text="Find the optimal STM pass combination for the next month",
                        font=('Arial', 18, 'bold'), bg="#00AEEF", fg="white")
main_heading.pack()

# Subheading
subheading = tk.Label(header_frame, text="This site allows you to get the price and find the optimal combination of STM passes over a period of 1 month from today's date.",
                      font=font_style, bg="#00AEEF", fg="white", wraplength=750, justify="center")
subheading.pack(pady=10)

# Image (Display metro.gif image)
img_path = "metro.gif"  # Update this path to the .gif image
try:
    # Open the image using Tkinter's PhotoImage (only for .gif format)
    img = tk.PhotoImage(file=img_path)
    img_label = tk.Label(root, image=img, bg="#E0F2F1")
    img_label.image = img  # Keep a reference to avoid garbage collection
    img_label.pack(pady=10)
except Exception as e:
    print(f"Error loading image: {e}")
    img_label = tk.Label(root, text="[Image could not be loaded]", font=font_style, bg="#E0F2F1")
    img_label.pack(pady=10)

# Description
description_frame = tk.Frame(root, bg="#E0F2F1", padx=30, pady=10)
description_frame.pack(fill="x")

description = tk.Label(description_frame, text="Enter a period by selecting a sequence of dates on the calendar. Then you can enter the number of passes per day over this period ",
                       font=font_style, bg="#E0F2F1", wraplength=750, justify="center")
description.pack()

# # Bullet points
# points = [
#     "the number of passes per day over this period"
# ]
# for point in points:
#     point_label = tk.Label(description_frame, text=f"- {point}", font=font_style, bg="#E0F2F1")
#     point_label.pack()

# Finish Frame (Continue button)
finish_frame = tk.Frame(root, bg="#E0F2F1", pady=20)
finish_frame.pack()

finish_button = tk.Button(finish_frame, text="Continue", font=bold_font, bg="#4CAF50", fg="white", relief="raised", bd=2, command=continue_action)
finish_button.pack(ipadx=20, ipady=10)

# Run the Tkinter event loop
root.mainloop()
