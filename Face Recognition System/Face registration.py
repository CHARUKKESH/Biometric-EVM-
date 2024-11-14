import cv2
import os
import sqlite3

# Database connection
def register_voter_in_db(name, aadhaar):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO voters (name, aadhaar) VALUES (?, ?)", (name, aadhaar))
        conn.commit()
        print(f"Voter {name} with Aadhaar {aadhaar} registered in the database.")
    except sqlite3.IntegrityError:
        print(f"A voter with Aadhaar {aadhaar} is already registered.")
    finally:
        conn.close()

# Function to capture and save face for registration
def register_voter(name, aadhaar_number):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    save_folder = "registered_voters/"
    os.makedirs(save_folder, exist_ok=True)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Register Voter', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                face_img = frame[y:y + h, x:x + w]
                filename = f"{name}_{aadhaar_number}.jpg"
                cv2.imwrite(os.path.join(save_folder, filename), face_img)
                print(f"Voter registered and image saved as {filename}")
                register_voter_in_db(name, aadhaar_number)
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    name = input("Enter Voter's Name: ")
    aadhaar = input("Enter Aadhaar Number: ")
    register_voter(name, aadhaar)