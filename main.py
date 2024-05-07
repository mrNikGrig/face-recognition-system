from deepface import DeepFace as df
import cv2
import time


def is_foto_in_db(path):
    # подгрузка файла из db
    for i in range(1, 5): # тут должны данные братся из дб
        similar = 0
        different = 0
        result = df.verify(img1_path=path,
            img2_path="images/" + str(i)+".jpg",
            model_name="Facenet512", enforce_detection=False)
        if result["verified"] == True:
            similar += 1
        else:
            different += 1
    return (similar > different)


def main():
    cap = cv2.VideoCapture(1)
    time.sleep(10)
    while True:
        ret, frame = cap.read()
        cv2.imwrite('image.jpg', frame)
        print(is_foto_in_db("image.jpg"))
        cv2.imshow("Камера", frame)


if __name__ == "__main__":
    main()
