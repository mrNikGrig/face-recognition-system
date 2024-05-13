from deepface import DeepFace as df
import sqlwork
import cv2
import time
import sqlite3
import tempfile
import os
from PIL import Image
import io


def is_foto_in_db(path, database_path):
    # Подключаемся к базе данных
    conn = sqlite3.connect(database_path)
    cursor = conn.cursor()

    # Переменные для подсчета сравнений
    similar = 0
    different = 0

    # Запрос на получение всех изображений из базы данных
    cursor.execute("SELECT image1, image2, image3, image4 FROM users")

    # Перебор всех записей в базе данных
    for row in cursor.fetchall():
        for i in range(4):  # У нас 4 колонки изображений
            # Получение бинарных данных изображения
            image_data = row[i]

            # Создание временного файла для изображения
            with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
                tmp_file.write(image_data)
                tmp_file_path = tmp_file.name

            # Сравнение изображений
            result = df.verify(img1_path=path,
                               img2_path=tmp_file_path,
                               model_name="Facenet512", enforce_detection=False)

            if result["verified"]:
                similar += 1
            else:
                different += 1

            # Удаляем временный файл
            os.remove(tmp_file_path)

    # Закрываем подключение к базе данных
    conn.close()

    # Возвращаем результат сравнения
    return (similar > different)


def main():
    while True:
        cmd = input(
            "Enter the required key to start working\n1. to start the system\n2. to add a person\n3. to delete a person\n4. to create a database if it doesn’t exist yet")
        if cmd == "1":
            cap = cv2.VideoCapture(0)
            time.sleep(2)
            while True:
                ret, frame = cap.read()
                if not ret:
                    break  # если не удалось получить кадр, прервать цикл
                cv2.imwrite('image.jpg', frame)

                print(is_foto_in_db("image.jpg"))
                cv2.imshow("Камера", frame)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    cv2.destroyAllWindows()
                    break

            cap.release()
            cv2.destroyAllWindows()
        elif cmd == "2":
            id = input("enter id person")
            full_name = input("enter full name")
            foto_1 = input("enter path to foto 1")
            foto_2 = input("enter path to foto 2")
            foto_3 = input("enter path to foto 3")
            foto_4 = input("enter path to foto 4")
            sqlwork.insertInTable(id, full_name, foto_1, foto_2, foto_3, foto_4)
        elif cmd == "3":
            delete_person = input("to delete person enter name/id")
            try:
                if type(delete_person) == int:
                    sqlwork.delete_person(id=delete_person)
                elif type(delete_person) == str:
                    sqlwork.delete_person(full_name=delete_person)
            except:
                print("wrong data")
        elif cmd == "4":
            sqlwork.tableCreating()


if __name__ == "__main__":
    main()
