import tkinter as tk
from tkinter import messagebox
import json
import os
from datetime import datetime

# initializes the list.
bills = []

# Checks if the .json file exists
# the .json file stores and loads the data.
BILLS_FILE = "bills.json"

# Load existing bills if the file exists
if os.path.exists(BILLS_FILE):
    with open(BILLS_FILE, "r") as f:
        try:
            bills = json.load(f)
        except json.JSONDecodeError:
            bills = []

# Function to calculate and store bill
def calculate_bill(pid, name, doctor, consult, medicine, room, days, payment_method, payment_details, date):
    try:
        consult = float(consult)
        medicine = float(medicine)
        room = float(room)
        days = int(days)
        room_total = room * days
        total = consult + medicine + room_total

        bill = {
            "patient_id": pid,
            "name": name,
            "doctor": doctor,
            "consultation_fee": consult,
            "medicine_cost": medicine,
            "room_charges": room,
            "days_admitted": days,
            "payment_method": payment_method,
            "payment_details": payment_details,
            "total": total,
            "date": date
        }

        bills.append(bill)

        # Saves the bill to the .json file
        with open(BILLS_FILE, "w") as f:
            json.dump(bills, f, indent=4)

        return bill

    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numbers for costs and days.")
        return None

# GUI Setup
def create_gui():
    window = tk.Tk()
    window.title("Hospital Billing System")
    window.geometry("520x750")
    window.config(bg="#f0f4f8", padx=20, pady=20)

    # Title
    tk.Label(window, text="🏥 Patient Billing System", font=("Helvetica", 18, "bold"),
             fg="#2e7d32", bg="#f0f4f8").pack(pady=10)

    # Input Frame
    frame = tk.Frame(window, bg="#f0f4f8")
    frame.pack(pady=10)

    label_font = ("Helvetica", 12)
    entry_font = ("Helvetica", 12)

    def create_row(row, text):
        tk.Label(frame, text=text, font=label_font, bg="#f0f4f8").grid(row=row, column=0, sticky="w", pady=5)
        entry = tk.Entry(frame, font=entry_font, width=25)
        entry.grid(row=row, column=1, pady=5)
        return entry
#these are the input boxes.
    entry_pid = create_row(0, "Patient ID")
    entry_name = create_row(1, "Patient Name")
    entry_doctor = create_row(2, "Doctor Name")
    entry_consult = create_row(3, "Consultation Fee")
    entry_medicine = create_row(4, "Medicine Cost")
    entry_room = create_row(5, "Room Charges (per day)")
    entry_days = create_row(6, "Days Admitted")

    # Payment Method Dropdown
    tk.Label(frame, text="Payment Method", font=label_font, bg="#f0f4f8").grid(row=7, column=0, sticky="w", pady=5)
    payment_var = tk.StringVar()
    payment_dropdown = tk.OptionMenu(frame, payment_var, "Cash", "Mpesa", "Card", "Insurance")
    payment_dropdown.config(font=("Helvetica", 11), width=20)
    payment_dropdown.grid(row=7, column=1, pady=5)
    payment_var.set("Cash")  # default

    # Dynamic Payment Details Frame
    payment_frame = tk.Frame(window, bg="#f0f4f8")
    payment_frame.pack()

    dynamic_entries = {}  # holds references to dynamic fields

    # Show/Hide fields depending on the payment type
    def update_payment_fields(*args):
        for widget in payment_frame.winfo_children():
            widget.destroy()
        dynamic_entries.clear()

        method = payment_var.get()
        if method == "Mpesa":
            tk.Label(payment_frame, text="Mpesa Phone No.", font=label_font, bg="#f0f4f8").grid(row=0, column=0, sticky="w", pady=5)
            mpesa_entry = tk.Entry(payment_frame, font=entry_font, width=25)
            mpesa_entry.grid(row=0, column=1, pady=5)
            dynamic_entries["mpesa_phone"] = mpesa_entry

        elif method == "Card":
            tk.Label(payment_frame, text="Card Number", font=label_font, bg="#f0f4f8").grid(row=0, column=0, sticky="w", pady=5)
            card_num = tk.Entry(payment_frame, font=entry_font, width=25)
            card_num.grid(row=0, column=1, pady=5)
            tk.Label(payment_frame, text="Card Holder Name", font=label_font, bg="#f0f4f8").grid(row=1, column=0, sticky="w", pady=5)
            card_name = tk.Entry(payment_frame, font=entry_font, width=25)
            card_name.grid(row=1, column=1, pady=5)
            dynamic_entries["card_number"] = card_num
            dynamic_entries["card_name"] = card_name

        elif method == "Insurance":
            tk.Label(payment_frame, text="Insurance Provider", font=label_font, bg="#f0f4f8").grid(row=0, column=0, sticky="w", pady=5)
            insurance_var = tk.StringVar()
            insurance_dropdown = tk.OptionMenu(payment_frame, insurance_var, "Jubilee", "APA", "AAR", "Britam", "CIC", "UAP Old Mutual", "Madison", "Heritage")
            insurance_dropdown.config(font=("Helvetica", 11), width=22)
            insurance_dropdown.grid(row=0, column=1, pady=5)
            insurance_var.set("Jubilee")
            dynamic_entries["insurance"] = insurance_var

    payment_var.trace("w", update_payment_fields)
    update_payment_fields()

    invoice_label = tk.Label(window, text="", justify="left", font=("Courier New", 11),
                             bg="#f0f4f8", fg="#333333")
    invoice_label.pack(pady=20)

    # Function to handle Generate Bill
    def on_generate():
        pid = entry_pid.get()
        name = entry_name.get()
        doctor = entry_doctor.get()
        consult = entry_consult.get()
        medicine = entry_medicine.get()
        room = entry_room.get()
        days = entry_days.get()
        payment_method = payment_var.get()
        date = datetime.now().strftime("%Y-%m-%d")

        # Collect extra payment details
        payment_details = ""
        if payment_method == "Mpesa":
            payment_details = dynamic_entries["mpesa_phone"].get()
        elif payment_method == "Card":
            card_number = dynamic_entries["card_number"].get()
            card_name = dynamic_entries["card_name"].get()
            payment_details = f"{card_name} - {card_number}"
        elif payment_method == "Insurance":
            payment_details = dynamic_entries["insurance"].get()

        if not all([pid, name, doctor, consult, medicine, room, days]):
            messagebox.showwarning("Missing Data", "Please fill in all required fields.")
            return

        bill = calculate_bill(pid, name, doctor, consult, medicine, room, days, payment_method, payment_details, date)
        if bill:
            invoice_text = f"""
--- INVOICE ---
Date       : {bill['date']}
Patient ID : {bill['patient_id']}
Name       : {bill['name']}
Doctor     : {bill['doctor']}
---------------------------
Consultation Fee : {bill['consultation_fee']}
Medicine Cost    : {bill['medicine_cost']}
Room Charges     : {bill['room_charges']} x {bill['days_admitted']} days
---------------------------
Payment Method   : {bill['payment_method']}
Payment Details  : {bill['payment_details']}
TOTAL BILL       : {bill['total']}
---------------------------
"""
            invoice_label.config(text=invoice_text)

    tk.Button(window, text="Generate Invoice", command=on_generate,
              bg="#4CAF50", fg="white", font=("Helvetica", 12, "bold"),
              padx=10, pady=5).pack(pady=10)

    window.mainloop()

if __name__ == "__main__":
    create_gui()
