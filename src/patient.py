import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# Global patient list
patients = []

# File path for storing patient data
DATA_FILE = "data/patients.json"

# Load existing patients from file
def load_patients():
    global patients
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            try:
                patients[:] = json.load(f)
            except json.JSONDecodeError:
                patients[:] = []

# Save updated patients to file
def save_patients():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # Ensure folder exists
    with open(DATA_FILE, 'w') as f:
        json.dump(patients, f, indent=4)

# Register new patient
def register_patient():
    name = entry_name.get()
    age = entry_age.get()
    gender = gender_var.get()
    condition = entry_condition.get()

    if not name or not age or not gender or not condition:
        messagebox.showerror("Missing Info", "Please fill all fields.")
        return

    try:
        age = int(age)
    except ValueError:
        messagebox.showerror("Invalid Input", "Age must be a number.")
        return

    patient = {
        "id": len(patients) + 1,
        "name": name,
        "age": age,
        "gender": gender,
        "condition": condition
    }

    patients.append(patient)
    save_patients()
    messagebox.showinfo("Success", f"Patient '{name}' registered.")
    clear_fields()
    view_patients()

# View all patients in table
def view_patients():
    load_patients()
    for row in tree.get_children():
        tree.delete(row)
    for p in patients:
        tree.insert('', tk.END, values=(p["id"], p["name"], p["age"], p["gender"], p["condition"]))

# Clear input fields
def clear_fields():
    entry_name.delete(0, tk.END)
    entry_age.delete(0, tk.END)
    entry_condition.delete(0, tk.END)
    gender_var.set("")

# GUI layout
def create_patient_gui():
    global entry_name, entry_age, entry_condition, gender_var, tree

    window = tk.Tk()
    window.title("Patient Registration System")
    window.geometry("720x500")
    window.configure(bg="#f4f6f8")

    style = ttk.Style()
    style.configure("TLabel", font=("Segoe UI", 11), background="#f4f6f8")
    style.configure("TEntry", font=("Segoe UI", 11))
    style.configure("TButton", font=("Segoe UI", 11), padding=6)
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    style.configure("Treeview", font=("Segoe UI", 10))

    frame = ttk.Frame(window, padding=20)
    frame.pack(fill=tk.BOTH, expand=True)

    # Row 0 - Name
    ttk.Label(frame, text="Patient Name:").grid(row=0, column=0, sticky="w", pady=4)
    entry_name = ttk.Entry(frame, width=30)
    entry_name.grid(row=0, column=1, pady=4)

    # Row 1 - Age
    ttk.Label(frame, text="Age:").grid(row=1, column=0, sticky="w", pady=4)
    entry_age = ttk.Entry(frame, width=30)
    entry_age.grid(row=1, column=1, pady=4)

    # Row 2 - Gender
    ttk.Label(frame, text="Gender:").grid(row=2, column=0, sticky="w", pady=4)
    gender_var = tk.StringVar()
    gender_frame = ttk.Frame(frame)
    gender_frame.grid(row=2, column=1, pady=4, sticky="w")
    ttk.Radiobutton(gender_frame, text="Male", variable=gender_var, value="Male").pack(side=tk.LEFT, padx=5)
    ttk.Radiobutton(gender_frame, text="Female", variable=gender_var, value="Female").pack(side=tk.LEFT, padx=5)

    # Row 3 - Condition
    ttk.Label(frame, text="Condition:").grid(row=3, column=0, sticky="w", pady=4)
    entry_condition = ttk.Entry(frame, width=30)
    entry_condition.grid(row=3, column=1, pady=4)

    # Row 4 - Buttons
    button_frame = ttk.Frame(frame)
    button_frame.grid(row=4, columnspan=2, pady=10)
    ttk.Button(button_frame, text="Register Patient", command=register_patient).pack(side=tk.LEFT, padx=5)
    ttk.Button(button_frame, text="Clear Fields", command=clear_fields).pack(side=tk.LEFT, padx=5)

    # Row 5 - Table
    tree = ttk.Treeview(frame, columns=("ID", "Name", "Age", "Gender", "Condition"), show="headings", height=8)
    for col in tree["columns"]:
        tree.heading(col, text=col)
        tree.column(col, width=100 if col != "Condition" else 200)
    tree.grid(row=5, column=0, columnspan=2, pady=20)

    load_patients()
    view_patients()

    window.mainloop()

# Run the GUI
if __name__ == "__main__":
    create_patient_gui()
