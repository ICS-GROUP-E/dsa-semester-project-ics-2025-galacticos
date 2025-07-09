import queue
import json
import os

class Doctor:
    def __init__(self, doctor_id, name, specialization, slots):
        self.doctor_id = doctor_id
        self.name = name
        self.specialization = specialization
        self.slots = slots  # List of available time slots
        self.appointments = queue.Queue()  # Queue of patient names

    def to_dict(self):
        return {
            "doctor_id": self.doctor_id,
            "name": self.name,
            "specialization": self.specialization,
            "slots": self.slots,
            "appointments": list(self.appointments.queue)
        }

    @staticmethod
    def from_dict(data):
        doc = Doctor(
            data["doctor_id"],
            data["name"],
            data["specialization"],
            data["slots"]
        )
        for patient in data["appointments"]:
            doc.appointments.put(patient)
        return doc


class DoctorManager:
    def __init__(self, filepath='data/doctors.json'):
        self.filepath = filepath
        self.doctors = {}
        self.load_data()

    def add_doctor(self, doctor):
        self.doctors[doctor.doctor_id] = doctor
        self.save_data()

    def get_doctor(self, doctor_id):
        return self.doctors.get(doctor_id)

    def schedule_appointment(self, doctor_id, patient_name):
        doctor = self.get_doctor(doctor_id)
        if doctor:
            doctor.appointments.put(patient_name)
            self.save_data()
            return True
        return False

    def next_patient(self, doctor_id):
        doctor = self.get_doctor(doctor_id)
        if doctor and not doctor.appointments.empty():
            patient = doctor.appointments.get()
            self.save_data()
            return patient
        return None

    def save_data(self):
        data = {doc_id: doc.to_dict() for doc_id, doc in self.doctors.items()}
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, 'w') as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                data = json.load(f)
                for doc_id, doc_data in data.items():
                    self.doctors[doc_id] = Doctor.from_dict(doc_data)
