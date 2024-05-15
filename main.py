from deepface import DeepFace as df
import sqlwork
import cv2
import time
import sqlite3
import tempfile
import os
from PIL import Image
import io


def get_user_by_id(user_id, database_path):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    cursor.execute("SELECT full_name FROM People WHERE id=?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    return user[0] if user else None


def is_foto_in_db(path, database_path="SQLite.db"):
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    similar_count = {}
    different_count = {}

    cursor.execute("SELECT id, image1, image2, image3, image4 FROM People")
    for row in cursor.fetchall():
        user_id = row[0]
        similar_count[user_id] = 0
        different_count[user_id] = 0
        for i in range(1, 5):
            image_data = row[i]
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(image_data)
                tmp_file_path = tmp_file.name
            result = df.verify(img1_path=path,
                               img2_path=tmp_file_path,
                               model_name="Facenet512", enforce_detection=False)
            if result["verified"]:
                similar_count[user_id] += 1
            else:
                different_count[user_id] += 1
            os.remove(tmp_file_path)

    conn.close()

    eligible_users = [user_id for user_id in similar_count if similar_count[user_id] >= 2]
    if eligible_users:
        user_names = [get_user_by_id(user_id, database_path) for user_id in eligible_users]
        return user_names
    else:
        return None


def main():
    while True:
        cmd = input("Enter the required key to start working\n1. to start the system\n2. to add a person\n3. to delete a person\n4. to create a database if it doesn’t exist yet\n")
        if cmd == "1":
            cap = cv2.VideoCapture(0)
            time.sleep(2)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                cv2.imwrite('image.jpg', frame)
                print(is_foto_in_db("image.jpg"))
                cv2.imshow("Camera", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            cap.release()
            cv2.destroyAllWindows()
        elif cmd == "2":
            id = input("enter id person\n")
            full_name = input("enter full name\n")
            foto_1 = input("enter path to foto 1\n")
            foto_2 = input("enter path to foto 2\n")
            foto_3 = input("enter path to foto 3\n")
            foto_4 = input("enter path to foto 4\n")
            sqlwork.insertInTable(id, full_name, foto_1, foto_2, foto_3, foto_4)
        elif cmd == "3":
            delete_person = input("to delete person enter name/id\n")
            try:
                if type(delete_person) == int:
                    sqlwork.delete_person(id=delete_person)
                elif type(delete_person) == str:
                    sqlwork.delete_person(full_name=delete_person)
            except:
                print("wrong data\n")
        elif cmd == "4":
            sqlwork.tableCreating()


if __name__ == "__main__":
    main()
