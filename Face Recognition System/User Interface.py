import tkinter as tk
from tkinter import messagebox
from face_registration import register_voter
from face_verification import verify_voter

# Function to handle voter registration from the GUI
def gui_register_voter():
    name = entry_name.get()
    aadhaar = entry_aadhaar.get()
    if name and aadhaar:
        register_voter(name, aadhaar)
        messagebox.showinfo("Success", f"Voter {name} registered successfully!")
    else:
        messagebox.showerror("Error", "Please enter both name and Aadhaar number.")

# Function to handle voter verification from the GUI
def gui_verify_voter():
    aadhaar = entry_aadhaar_verify.get()
    if aadhaar:
        verify_voter(aadhaar)
    else:
        messagebox.showerror("Error", "Please enter Aadhaar number for verification.")

# Tkinter Window
root = tk.Tk()
root.title("Voting System")

# Registration GUI
frame_registration = tk.Frame(root)
frame_registration.pack(pady=10)

label_name = tk.Label(frame_registration, text="Voter Name:")
label_name.grid(row=0, column=0)
entry_name = tk.Entry(frame_registration)
entry_name.grid(row=0, column=1)

label_aadhaar = tk.Label(frame_registration, text="Aadhaar Number:")
label_aadhaar.grid(row=1, column=0)
entry_aadhaar = tk.Entry(frame_registration)
entry_aadhaar.grid(row=1, column=1)

button_register = tk.Button(frame_registration, text="Register Voter", command=gui_register_voter)
button_register.grid(row=2, columnspan=2, pady=5)

# Verification GUI
frame_verification = tk.Frame(root)
frame_verification.pack(pady=10)

label_aadhaar_verify = tk.Label(frame_verification, text="Enter Aadhaar for Voting:")
label_aadhaar_verify.grid(row=0, column=0)
entry_aadhaar_verify = tk.Entry(frame_verification)
entry_aadhaar_verify.grid(row=0, column=1)

button_verify = tk.Button(frame_verification, text="Verify & Vote", command=gui_verify_voter)
button_verify.grid(row=1, columnspan=2, pady=5)

root.mainloop()