from deepface import DeepFace as df
import pickle
import time
import cv2
import os


def main():
    for i in range(1, 7):
        for j in range(1, 7):
            result = df.verify(img1_path="images/" + str(i) +".jpg",
                                     img2_path="images/" + str(j)+".jpg",
                                     model_name="VGG-Face", enforce_detection=False)
            print(i, j, result['verified'])


if __name__ == "__main__":
    main()
