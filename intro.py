from tkinter import *
from tkinter.ttk import Combobox
from datetime import datetime, timedelta

# Initialize the main application window
root = Tk()
root.title("Interactive Custom Calendar")
root.geometry("1000x700")

# Global Variables
period_data = {}  # Stores data for each period
button_map = {}  # Maps buttons to dates
selected_dates = {}  # Tracks which dates are selected by which period
today_date = datetime.now().date()
max_date = today_date + timedelta(days=30)
is_shift_pressed = False  # Tracks if Shift key is pressed
first_selected_date = None  # Tracks the first clicked date

# Define 25 unique colors for the passes
color_map = [
    "#00A94F", "#00AEEF", "#7A1F7E", "#C6D8D3", "#FFE512",
    "#00FF7F", "#00FFFF", "#007FFF", "#0000FF", "#7F00FF",
    "#FF00FF", "#FF007F", "#B22222", "#FF4500", "#DA70D6",
    "#9370DB", "#8A2BE2", "#5F9EA0", "#7FFF00", "#FFD700",
    "#FF69B4", "#CD5C5C", "#4B0082", "#6A5ACD", "#708090"
]

# Reset the calendar and reapply date restrictions
def reset_calendar():
    global selected_dates
    selected_dates.clear()  # Clear all selected dates
    for date_str, btn in button_map.items():
        # Reapply the range restrictions
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        if today_date <= date_obj <= max_date:
            btn.config(bg="white", fg="black", state=NORMAL)
        else:
            btn.config(bg="lightgrey", fg="black", state=DISABLED)

# Select a date on the calendar
def select_date(date_str):
    if not period_data:
        return

    active_period_id = max(period_data.keys())
    dropdown_value = int(period_data[active_period_id]["dropdown"].get())

    # Use predefined color based on the dropdown value
    color = color_map[dropdown_value - 1]

    # Update the selected date for the active period
    if date_str not in selected_dates:
        period_data[active_period_id]["dates"].add(date_str)
        selected_dates[date_str] = {"period": active_period_id, "color": color, "pass": dropdown_value}
        button_map[date_str].config(bg=color, fg="white")

# Handle date click and range selection
def on_date_click(event):
    global first_selected_date, is_shift_pressed
    widget = event.widget
    if isinstance(widget, Button) and hasattr(widget, 'date_str'):
        date_str = widget.date_str

        # If Shift is pressed, select the range
        if is_shift_pressed and first_selected_date:
            start_date = datetime.strptime(first_selected_date, "%Y-%m-%d").date()
            end_date = datetime.strptime(date_str, "%Y-%m-%d").date()
            for date_key, btn in button_map.items():
                current_date = datetime.strptime(date_key, "%Y-%m-%d").date()
                if start_date <= current_date <= end_date or end_date <= current_date <= start_date:
                    select_date(date_key)
        else:
            # If Shift is not pressed, update the first selected date
            first_selected_date = date_str
            select_date(date_str)

# Update Shift key state
def on_key_press(event):
    global is_shift_pressed
    if event.keysym in ("Shift_L", "Shift_R"):
        is_shift_pressed = True

# Update Shift key state
def on_key_release(event):
    global is_shift_pressed
    if event.keysym in ("Shift_L", "Shift_R"):
        is_shift_pressed = False

# Update color dynamically based on dropdown selection
def update_color(period_id):
    dropdown_value = int(period_data[period_id]["dropdown"].get())
    color = color_map[dropdown_value - 1]
    period_data[period_id]["color_box"].config(bg=color)


import os 
file_path = r'C:\Users\victo\Documents\web projects\Opus website\selected_dates.txt'
if os.path.exists(file_path):
    os.remove(file_path)  # Delete the file if it exists
    

import subprocess

# Generate output file
def generate_output_file():
    output_path = r'C:\Users\victo\Documents\web projects\Opus website\selected_dates.txt'

            # Write as a list of lists


    try:
        with open(output_path, "w") as file:
            items = [f"['{date_str}', {data['pass']}]" for date_str, data in selected_dates.items()]
            formatted_output = "[" + ", ".join(items) + "]"
            file.write(formatted_output + "\n")
        
         # Run message.txt to calculate the best combination
        subprocess.run(["python", "basic_no_bugs.py"])
        
    except Exception as e:
        print(f"Error generating file: {e}")

# Create a single month calendar
def create_month_calendar(month, year, row_offset):
    global button_map
    Label(calendar_frame, text=f"{datetime(year, month, 1):%B %Y}", font=("Arial", 14, "bold")).grid(row=row_offset, column=0, columnspan=7, pady=10)

    # Weekdays header
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for col, day in enumerate(days):
        Label(calendar_frame, text=day, font=("Arial", 10, "bold")).grid(row=row_offset + 1, column=col)

    # Determine first weekday and total days
    first_day = datetime(year, month, 1)
    first_weekday = (first_day.weekday() + 1) % 7
    total_days = (datetime(year, month + 1, 1) - timedelta(days=1)).day if month < 12 else 31

    # Add days to the grid
    row, col = row_offset + 2, first_weekday
    for day in range(1, total_days + 1):
        date_obj = datetime(year, month, day).date()
        date_str = date_obj.strftime("%Y-%m-%d")
        is_selectable = today_date <= date_obj <= max_date

        # Create the button
        btn = Button(
            calendar_frame,
            text=str(day),
            width=5,
            bg="white" if is_selectable else "lightgrey",
            state=NORMAL if is_selectable else DISABLED
        )
        btn.date_str = date_str  # Attach date string to button
        btn.grid(row=row, column=col, padx=2, pady=2)
        btn.bind("<Button-1>", on_date_click)  # Bind left click to date click handler
        button_map[date_str] = btn

        col += 1
        if col > 6:  # Next row after Sunday
            col = 0
            row += 1

    return row - row_offset + 2

# Create the calendar grid for two months
def create_calendar():
    global button_map
    button_map.clear()
    for widget in calendar_frame.winfo_children():
        widget.destroy()

    current_month = today_date.month
    next_month = (current_month % 12) + 1
    current_year = today_date.year
    next_year = current_year if next_month > current_month else current_year + 1

    # Populate both months
    row_offset = 0
    for month, year in [(current_month, current_year), (next_month, next_year)]:
        row_offset += create_month_calendar(month, year, row_offset)

# Save a period
def save_period(period_id):
    if period_id in period_data:
        # Error if no dates are selected
        if not period_data[period_id]["dates"]:
            if "error_label" not in period_data[period_id]:
                error_label = Label(main_frame, text="Please select a date", fg="red")
                error_label.grid(row=period_id, column=4, padx=10)
                period_data[period_id]["error_label"] = error_label
            return

        # Remove error message if exists
        if "error_label" in period_data[period_id]:
            period_data[period_id]["error_label"].destroy()
            del period_data[period_id]["error_label"]

        period_data[period_id]["saved"] = True
        period_data[period_id]["dropdown"].config(state="disabled")

# Delete a period
def delete_period(period_id, widgets):
    if period_id in period_data:
        for date_str in list(period_data[period_id]["dates"]):
            if date_str in selected_dates and selected_dates[date_str]["period"] == period_id:
                del selected_dates[date_str]
                button_map[date_str].config(bg="white", fg="black")
        del period_data[period_id]

    for widget in widgets:
        widget.destroy()

    if not period_data:
        reset_calendar()

# Add a new period
def add_period():
    if period_data and not period_data[max(period_data.keys())]["saved"]:
        last_period_id = max(period_data.keys())
        if "error_label" not in period_data[last_period_id]:
            error_label = Label(main_frame, text="Save the previous period first", fg="red")
            error_label.grid(row=last_period_id, column=4, padx=10)
            period_data[last_period_id]["error_label"] = error_label
        return

    period_id = len(period_data) + 1

    # Default color for the new period
    color = color_map[0]

    # Create period label with color box
    color_box = Label(main_frame, width=2, height=1, bg=color, relief="solid")
    color_box.grid(row=period_id, column=0, padx=5, pady=5)

    period_label = Label(main_frame, text="Period")
    period_label.grid(row=period_id, column=1, padx=10, pady=5)

    dropdown = Combobox(main_frame, values=list(range(1, 26)), state="readonly")
    dropdown.set("1")
    dropdown.grid(row=period_id, column=2, padx=10, pady=5)
    dropdown.bind("<<ComboboxSelected>>", lambda e, p=period_id: update_color(p))

    save_btn = Button(main_frame, text="Save", command=lambda: save_period(period_id))
    save_btn.grid(row=period_id, column=3, padx=10, pady=5)

    delete_btn = Button(main_frame, text="🗑️", command=lambda: delete_period(period_id, [color_box, period_label, dropdown, save_btn, delete_btn]))
    delete_btn.grid(row=period_id, column=4, padx=10, pady=5)

    period_data[period_id] = {"label": period_label, "dropdown": dropdown, "dates": set(), "saved": False, "color_box": color_box}

    for date_str, btn in button_map.items():
        # Ensure only dates within the valid range are clickable
        date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()
        is_selectable = today_date <= date_obj <= max_date
        btn.config(state=NORMAL if is_selectable else DISABLED)

# Frames
header_frame = Frame(root)
header_frame.pack()

calendar_frame = Frame(root)
calendar_frame.pack()

main_frame = Frame(root)
main_frame.pack(pady=20)

# Titles
Label(main_frame, text="Periods", font=("Arial", 14, "bold")).grid(row=0, column=1, padx=10)
Label(main_frame, text="Passes", font=("Arial", 14, "bold")).grid(row=0, column=2, padx=10)

# Buttons
Button(root, text="+ Add Period", command=add_period).pack(pady=10)
Button(header_frame, text="Calculate", bg='lightgreen', command=generate_output_file).pack(side='left', anchor='n', pady=10)

# Bind Shift key events
root.bind("<KeyPress>", on_key_press)
root.bind("<KeyRelease>", on_key_release)

# Initialize
create_calendar()


root.mainloop()



