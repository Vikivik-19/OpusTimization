import tkinter as tk
from tkinter import messagebox
import subprocess

def submit():
    try:
        # Retrieve and validate the inputs
        age = int(age_entry.get())
        student_status = student_var.get()

        if age <= 0:
            raise ValueError("Please enter a valid age greater than 0.")

        # Save the information to a text file
        with open("user_info.txt", "w") as file:
            file.write(f"{age}\n{student_status}")

        # Display the collected information
        messagebox.showinfo("Your Information",
                            f"Your age: {age}\nStudent status: {student_status}")

        # Run the intro.py script
        subprocess.run(['python', 'intro.py'], check=True)

    except ValueError as e:
        # Show error message if inputs are invalid
        messagebox.showerror("Invalid Input", str(e))
    except Exception as e:
        # Show error message if there is an issue running intro.py
        messagebox.showerror("Error", f"Failed to run intro.py: {e}")


# Create the main window
root = tk.Tk()
root.title("User Information")
root.geometry("800x500")  # Make the window larger for a spacious layout
root.minsize(800, 500)

# Set modern fonts with stylish combos
font_style = ('Helvetica', 14)
bold_font = ('Helvetica', 16, 'bold')

# Set the pale blue color for the background
root.config(bg="#E0F2F1")  # Pale blue background

# Frame for content with a cleaner and rounded border
frame = tk.Frame(root, padx=30, pady=30, bg="#ffffff", bd=5, relief="solid", highlightthickness=0)
frame.place(relx=0.5, rely=0.5, anchor='center')

# Title label with larger font and gradient blue
title_label = tk.Label(frame, text="User Information Form", font=('Helvetica', 20, 'bold'), bg="#ffffff", fg="#00AEEF")
title_label.grid(row=0, column=0, columnspan=2, pady=30)

# Age input label and entry field with rounded corners and a refined look
age_label = tk.Label(frame, text="Please enter your age:", font=font_style, bg="#ffffff", fg="#333")
age_label.grid(row=1, column=0, sticky="w", pady=20)
age_entry = tk.Entry(frame, font=font_style, width=25, bd=2, relief="solid", highlightbackground="#1E3A8A", highlightthickness=2)
age_entry.grid(row=1, column=1, pady=20)

# Student status label with a modern blue look
student_label = tk.Label(frame, text="Are you a student?", font=font_style, bg="#ffffff", fg="#333")
student_label.grid(row=2, column=0, sticky="w", pady=20)

# Student status radio buttons with larger options and modern blue
student_var = tk.StringVar(value="No")
student_yes = tk.Radiobutton(frame, text="Yes", variable=student_var, value="Yes", font=font_style, bg="#ffffff", fg="#1E3A8A", activebackground="#e6f2ff")
student_yes.grid(row=2, column=1, sticky="w")
student_no = tk.Radiobutton(frame, text="No", variable=student_var, value="No", font=font_style, bg="#ffffff", fg="#1E3A8A", activebackground="#e6f2ff")
student_no.grid(row=3, column=1, sticky="w")

# Submit button with rounded corners, larger size, and bold text
submit_button = tk.Button(frame, text="Submit", command=submit, font=bold_font, bg="#00A94F", fg="white", relief="raised", bd=3, padx=30, pady=15, activebackground="#1E58D0")
submit_button.grid(row=4, column=0, columnspan=2, pady=30)

# Run the GUI loop
root.mainloop()

