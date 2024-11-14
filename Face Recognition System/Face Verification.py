import cv2
import os
from deepface import DeepFace
import sqlite3

# Connect to the database to check voting status
def check_voting_status(aadhaar):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, voted FROM voters WHERE aadhaar=?", (aadhaar,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0], result[1]  # Return name and voted status (0 or 1)
    return None, None

# Update the voting status in the database
def update_voting_status(aadhaar):
    conn = sqlite3.connect('voting_system.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE voters SET voted = 1 WHERE aadhaar=?", (aadhaar,))
    conn.commit()
    conn.close()

# Function to verify voter and check if they can vote
def verify_voter(aadhaar_number):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        cv2.imshow('Verify Voter', frame)

        if cv2.waitKey(1) & 0xFF == ord('s'):
            if len(faces) == 1:
                (x, y, w, h) = faces[0]
                face_img = frame[y:y + h, x:x + w]

                for filename in os.listdir("registered_voters/"):
                    voter_path = os.path.join("registered_voters/", filename)
                    result = DeepFace.verify(face_img, voter_path, model_name='VGG-Face')

                    if result['verified']:
                        name, registered_aadhaar = filename.split("")[0], filename.split("")[1].split(".")[0]
                        if aadhaar_number == registered_aadhaar:
                            voter_name, voted = check_voting_status(aadhaar_number)
                            if voted == 1:
                                print(f"{voter_name} has already voted!")
                            else:
                                print(f"{voter_name} is allowed to vote.")
                                update_voting_status(aadhaar_number)
                            return

            print("Unknown or unregistered person.")
            break

    cap.release()
    cv2.destroyAllWindows()

if _name_ == "_main_":
    aadhaar = input("Enter Aadhaar Number: ")
    verify_voter(aadhaar)