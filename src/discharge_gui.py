import tkinter as tk
from patient_discharge import launch_discharge_module


def main():
    root = tk.Tk()
    root.title("Hospital Management System")
    root.geometry("400x250")

    heading = tk.Label(root, text="Hospital Management System", font=("Helvetica", 16, "bold"))
    heading.pack(pady=20)

    btn_discharge = tk.Button(root, text="Search & Discharge Module", width=30, command=launch_discharge_module)
    btn_discharge.pack(pady=10)

    # Placeholder for future modules
    btn_exit = tk.Button(root, text="Exit", width=30, command=root.quit)
    btn_exit.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()
