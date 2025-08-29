from abc import ABC, abstractmethod
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta

# Abstraction: Abstract base class for hospital staff
class Hospitalstaff(ABC):
    @abstractmethod
    def get_details(self):
        pass

# Encapsulation: Patient class
class Patient:
    def __init__(self, patient_id, name, age, medical_history):
        self.__patient_id = patient_id  # Private attribute
        self.__name = name
        self.__age = age
        self.__medical_history = medical_history
        self.__appointments = []

    def get_patient_id(self):
        return self.__patient_id

    def get_name(self):
        return self.__name

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def get_details(self):
        return f"Patient: {self.__name}, ID: {self.__patient_id}, Age: {self.__age}, History: {self.__medical_history}"

# Inheritance and Polymorphism
class Doctor(Hospitalstaff):
    def __init__(self, doctor_id, name, specialty):
        self.__doctor_id = doctor_id
        self.__name = name
        self.__specialty = specialty
        self.__appointments = []

    def get_doctor_id(self):
        return self.__doctor_id

    def get_name(self):
        return self.__name

    def add_appointment(self, appointment):
        self.__appointments.append(appointment)

    def get_details(self):
        return f"Doctor: {self.__name}, ID: {self.__doctor_id}, Specialty: {self.__specialty}"

# Encapsulation:
class Appointment:
    def __init__(self, appointment_id, patient, doctor, date_time):
        self.__appointment_id = appointment_id
        self.__patient = patient
        self.__doctor = doctor
        self.__date_time = date_time

    def get_details(self):
        return f"Appointment ID: {self.__appointment_id}, Patient: {self.__patient.get_name()}, Doctor: {self.__doctor.get_name()}, Date: {self.__date_time.strftime('%Y-%m-%d %H:%M')}"

# Encapsulation: 
class Hospital:
    def __init__(self, name):
        self.__name = name  
        self.__patients = {}
        self.__doctors = {}
        self.__appointments = {}
        self.__history = []

    def add_patient(self, patient_id, name, age, medical_history):
        if patient_id not in self.__patients:
            self.__patients[patient_id] = Patient(patient_id, name, age, medical_history)
            self.__log_action(f"Added patient: {name} (ID: {patient_id})")
            return True
        return False

    def add_doctor(self, doctor_id, name, specialty):
        if doctor_id not in self.__doctors:
            self.__doctors[doctor_id] = Doctor(doctor_id, name, specialty)
            self.__log_action(f"Added doctor: {name} (ID: {doctor_id})")
            return True
        return False

    def schedule_appointment(self, appointment_id, patient_id, doctor_id, date_time):
        patient = self.__patients.get(patient_id)
        doctor = self.__doctors.get(doctor_id)
        if patient and doctor and appointment_id not in self.__appointments:
            appointment = Appointment(appointment_id, patient, doctor, date_time)
            self.__appointments[appointment_id] = appointment
            patient.add_appointment(appointment)
            doctor.add_appointment(appointment)
            self.__log_action(f"Scheduled appointment {appointment_id} for {patient.get_name()} with {doctor.get_name()}")
            return True
        return False

    def __log_action(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.__history.append(f"[{timestamp}] {message}")

    def get_summary(self):
        summary = [f"Hospital: {self.__name}"]
        summary.append("\nPatients:")
        for patient in self.__patients.values():
            summary.append(patient.get_details())
        summary.append("\nDoctors:")
        for doctor in self.__doctors.values():
            summary.append(doctor.get_details())
        summary.append("\nAppointments:")
        for appointment in self.__appointments.values():
            summary.append(appointment.get_details())
        return "\n".join(summary)

    def get_history(self):
        return self.__history if self.__history else ["No actions performed"]
class HospitalGUI:
    def __init__(self, root):
        self.__hospital = Hospital("City Health Center")
        self.__root = root
        self.__root.title("Hospital Management System")
        self.__root.geometry("600x500")
        self.__create_widgets()

    def __create_widgets(self):
        notebook = ttk.Notebook(self.__root)
        notebook.pack(pady=10, expand=True)
        patient_frame = ttk.Frame(notebook)
        notebook.add(patient_frame, text="Add Patient")
        self.__create_patient_form(patient_frame)
        doctor_frame = ttk.Frame(notebook)
        notebook.add(doctor_frame, text="Add Doctor")
        self.__create_doctor_form(doctor_frame)
        appointment_frame = ttk.Frame(notebook)
        notebook.add(appointment_frame, text="Schedule Appointment")
        self.__create_appointment_form(appointment_frame)
        summary_frame = ttk.Frame(notebook)
        notebook.add(summary_frame, text="View Summary")
        self.__create_summary_view(summary_frame)

    def __create_patient_form(self, frame):
        tk.Label(frame, text="Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        patient_id_entry = tk.Entry(frame)
        patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Age:").grid(row=2, column=0, padx=5, pady=5)
        age_entry = tk.Entry(frame)
        age_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Medical History:").grid(row=3, column=0, padx=5, pady=5)
        history_entry = tk.Entry(frame)
        history_entry.grid(row=3, column=1, padx=5, pady=5)

        def add_patient():
            try:
                patient_id = patient_id_entry.get()
                name = name_entry.get()
                age = int(age_entry.get())
                history = history_entry.get()
                if self.__hospital.add_patient(patient_id, name, age, history):
                    messagebox.showinfo("Success", "Patient added successfully")
                    patient_id_entry.delete(0, tk.END)
                    name_entry.delete(0, tk.END)
                    age_entry.delete(0, tk.END)
                    history_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Patient ID already exists")
            except ValueError:
                messagebox.showerror("Error", "Invalid age")

        tk.Button(frame, text="Add Patient", command=add_patient).grid(row=4, column=0, columnspan=2, pady=10)

    def __create_doctor_form(self, frame):
        tk.Label(frame, text="Doctor ID:").grid(row=0, column=0, padx=5, pady=5)
        doctor_id_entry = tk.Entry(frame)
        doctor_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Name:").grid(row=1, column=0, padx=5, pady=5)
        name_entry = tk.Entry(frame)
        name_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Specialty:").grid(row=2, column=0, padx=5, pady=5)
        specialty_entry = tk.Entry(frame)
        specialty_entry.grid(row=2, column=1, padx=5, pady=5)

        def add_doctor():
            doctor_id = doctor_id_entry.get()
            name = name_entry.get()
            specialty = specialty_entry.get()
            if self.__hospital.add_doctor(doctor_id, name, specialty):
                messagebox.showinfo("Success", "Doctor added successfully")
                doctor_id_entry.delete(0, tk.END)
                name_entry.delete(0, tk.END)
                specialty_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Doctor ID already exists")

        tk.Button(frame, text="Add Doctor", command=add_doctor).grid(row=3, column=0, columnspan=2, pady=10)

    def __create_appointment_form(self, frame):
        tk.Label(frame, text="Appointment ID:").grid(row=0, column=0, padx=5, pady=5)
        appointment_id_entry = tk.Entry(frame)
        appointment_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Patient ID:").grid(row=1, column=0, padx=5, pady=5)
        patient_id_entry = tk.Entry(frame)
        patient_id_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Doctor ID:").grid(row=2, column=0, padx=5, pady=5)
        doctor_id_entry = tk.Entry(frame)
        doctor_id_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
        date_entry = tk.Entry(frame)
        date_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Time (HH:MM):").grid(row=4, column=0, padx=5, pady=5)
        time_entry = tk.Entry(frame)
        time_entry.grid(row=4, column=1, padx=5, pady=5)

        def schedule_appointment():
            try:
                appointment_id = appointment_id_entry.get()
                patient_id = patient_id_entry.get()
                doctor_id = doctor_id_entry.get()
                date_time_str = f"{date_entry.get()} {time_entry.get()}"
                date_time = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M")
                if date_time < datetime.now():
                    messagebox.showerror("Error", "Cannot schedule appointment in the past")
                    return
                if self.__hospital.schedule_appointment(appointment_id, patient_id, doctor_id, date_time):
                    messagebox.showinfo("Success", "Appointment scheduled successfully")
                    appointment_id_entry.delete(0, tk.END)
                    patient_id_entry.delete(0, tk.END)
                    doctor_id_entry.delete(0, tk.END)
                    date_entry.delete(0, tk.END)
                    time_entry.delete(0, tk.END)
                else:
                    messagebox.showerror("Error", "Invalid IDs or appointment ID exists")
            except ValueError:
                messagebox.showerror("Error", "Invalid date/time format")

        tk.Button(frame, text="Schedule Appointment", command=schedule_appointment).grid(row=5, column=0, columnspan=2, pady=10)

    def __create_summary_view(self, frame):
        text_area = tk.Text(frame, height=20, width=60)
        text_area.grid(row=0, column=0, padx=5, pady=5)

        def show_summary():
            text_area.delete(1.0, tk.END)
            text_area.insert(tk.END, self.__hospital.get_summary())

        def show_history():
            history = "\n".join(self.__hospital.get_history())
            messagebox.showinfo("Action History", history if history else "No history available")

        tk.Button(frame, text="Show Summary", command=show_summary).grid(row=1, column=0, pady=5)
        tk.Button(frame, text="Show History", command=show_history).grid(row=2, column=0, pady=5)
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalGUI(root)
    root.mainloop()