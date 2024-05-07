from deepface import DeepFace as df
import time


def is_foto_in_db(path):
    # подгрузка файла из db
    for i in range(1, 5): # тут должны данные братся из дб
        similar= 0
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
    t = time.time()
    print(is_foto_in_db("images/7.jpg"), time.time()-t)


if __name__ == "__main__":
    main()
