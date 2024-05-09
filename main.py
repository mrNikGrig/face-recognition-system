from deepface import DeepFace as df
import cv2
import time

def is_foto_in_db(path):
    similar = 0
    different = 0
    for i in range(1, 5):
        result = df.verify(img1_path=path,
            img2_path="images/" + str(i) + ".jpg",
            model_name="Facenet512", enforce_detection=False)
        if result["verified"]:
            similar += 1
        else:
            different += 1
    return (similar > different)

def main():
    cap = cv2.VideoCapture(0)
    time.sleep(2)
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # если не удалось получить кадр, прервать цикл
        cv2.imwrite('image.jpg', frame)
        # Обнаружение лиц на кадре
        detected_faces = df.detectFace("image.jpg", enforce_detection=False)
        for face in detected_faces:
            x, y, w, h = face['x'], face['y'], face['width'], face['height']
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)


        print(is_foto_in_db("image.jpg"))
        cv2.imshow("Камера", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
