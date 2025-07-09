import tkinter as tk
from tkinter import ttk, messagebox
from doctor import Doctor, DoctorManager

manager = DoctorManager()

# UI utility functions
def refresh_doctor_dropdown():
    manager.load_data()
    doctor_dropdown['values'] = list(manager.doctors.keys())

def refresh_queue_display(event=None):
    doctor_id = doctor_dropdown.get()
    doctor = manager.get_doctor(doctor_id)
    if doctor:
        queue_display.delete(0, tk.END)
        for patient in list(doctor.appointments.queue):
            queue_display.insert(tk.END, patient)

def refresh_slot_dropdown():
    doctor_id = doctor_dropdown.get()
    doctor = manager.get_doctor(doctor_id)
    if doctor:
        slot_dropdown['values'] = doctor.slots

# Logic functions
def register_doctor():
    doctor_id = entry_id.get()
    name = entry_name.get()
    specialization = entry_specialization.get()
    slots = entry_slots.get().split(',')

    if not doctor_id or not name:
        messagebox.showerror("Error", "Doctor ID and Name are required")
        return

    doctor = Doctor(doctor_id, name, specialization, slots)
    manager.add_doctor(doctor)
    messagebox.showinfo("Success", f"Doctor {name} registered.")
    refresh_doctor_dropdown()
    entry_id.delete(0, tk.END)
    entry_name.delete(0, tk.END)
    entry_specialization.delete(0, tk.END)
    entry_slots.delete(0, tk.END)

def schedule_patient():
    doctor_id = doctor_dropdown.get()
    patient_name = entry_patient_name.get()
    selected_slot = slot_dropdown.get()

    if not doctor_id or not patient_name or not selected_slot:
        messagebox.showerror("Error", "All fields are required")
        return

    doctor = manager.get_doctor(doctor_id)
    if doctor:
        if selected_slot not in doctor.slots:
            messagebox.showerror("Error", "Selected slot is not available")
            return
        doctor.appointments.put(f"{patient_name} @ {selected_slot}")
        doctor.slots.remove(selected_slot)
        manager.save_data()
        messagebox.showinfo("Scheduled", f"{patient_name} booked for {selected_slot}")
        entry_patient_name.delete(0, tk.END)
        refresh_queue_display()
        refresh_slot_dropdown()
    else:
        messagebox.showerror("Error", "Doctor not found")

def serve_next_patient():
    doctor_id = doctor_dropdown.get()
    doctor = manager.get_doctor(doctor_id)
    if doctor and not doctor.appointments.empty():
        served = doctor.appointments.get()
        manager.save_data()
        messagebox.showinfo("Served", f"{served} has been served")
        refresh_queue_display()
    else:
        messagebox.showinfo("Queue Empty", "No patients in queue")

# GUI Setup
root = tk.Tk()
root.title("Doctor Management System")
root.geometry("600x600")
root.configure(bg="#f2f2f2")

notebook = ttk.Notebook(root)
frame_register = ttk.Frame(notebook, padding=20)
frame_appointment = ttk.Frame(notebook, padding=20)
notebook.add(frame_register, text="Register Doctor")
notebook.add(frame_appointment, text="Book Appointment")
notebook.pack(expand=True, fill='both', padx=10, pady=10)

# Register Doctor UI
ttk.Label(frame_register, text="Register New Doctor", font=("Segoe UI", 14, "bold")).pack(pady=10)

form = ttk.Frame(frame_register)
form.pack(pady=5)

ttk.Label(form, text="Doctor ID:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
entry_id = ttk.Entry(form, width=30)
entry_id.grid(row=0, column=1, padx=5)

ttk.Label(form, text="Name:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
entry_name = ttk.Entry(form, width=30)
entry_name.grid(row=1, column=1)

ttk.Label(form, text="Specialization:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
entry_specialization = ttk.Entry(form, width=30)
entry_specialization.grid(row=2, column=1)

ttk.Label(form, text="Time Slots (comma-separated):").grid(row=3, column=0, sticky='e', padx=5, pady=5)
entry_slots = ttk.Entry(form, width=30)
entry_slots.grid(row=3, column=1)

ttk.Button(frame_register, text="Add Doctor", command=register_doctor).pack(pady=10)

# Appointment Booking UI
ttk.Label(frame_appointment, text="Book Appointment", font=("Segoe UI", 14, "bold")).pack(pady=10)

appt_form = ttk.Frame(frame_appointment)
appt_form.pack(pady=5)

ttk.Label(appt_form, text="Select Doctor:").grid(row=0, column=0, sticky='e', padx=5, pady=5)
doctor_dropdown = ttk.Combobox(appt_form, state="readonly", width=28)
doctor_dropdown.grid(row=0, column=1)
doctor_dropdown.bind("<<ComboboxSelected>>", lambda e: [refresh_queue_display(), refresh_slot_dropdown()])

ttk.Label(appt_form, text="Available Time Slot:").grid(row=1, column=0, sticky='e', padx=5, pady=5)
slot_dropdown = ttk.Combobox(appt_form, state="readonly", width=28)
slot_dropdown.grid(row=1, column=1)

ttk.Label(appt_form, text="Patient Name:").grid(row=2, column=0, sticky='e', padx=5, pady=5)
entry_patient_name = ttk.Entry(appt_form, width=30)
entry_patient_name.grid(row=2, column=1)

ttk.Button(frame_appointment, text="Schedule Appointment", command=schedule_patient).pack(pady=10)
ttk.Button(frame_appointment, text="Serve Next Patient", command=serve_next_patient).pack()

ttk.Label(frame_appointment, text="Current Appointment Queue", font=("Segoe UI", 12)).pack(pady=(20, 5))
queue_display = tk.Listbox(frame_appointment, height=10, width=50, font=("Courier New", 10))
queue_display.pack()

# Final init
refresh_doctor_dropdown()
root.mainloop()
