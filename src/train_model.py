"""Train an LBPH face recognizer on the samples captured by capture_faces.py."""

import os

import cv2
import numpy as np

from . import config


def gather_training_data():
    faces = []
    ids = []

    for user_id in os.listdir(config.DATA_DIR):
        user_dir = os.path.join(config.DATA_DIR, user_id)
        if not os.path.isdir(user_dir):
            continue

        for filename in os.listdir(user_dir):
            image_path = os.path.join(user_dir, filename)
            image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            if image is None:
                continue
            faces.append(image)
            ids.append(int(user_id))

    return faces, ids


def train():
    faces, ids = gather_training_data()

    if not faces:
        print("No training data found. Run capture_faces.py first.")
        return

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(ids))
    recognizer.write(config.MODEL_PATH)

    print(f"Model trained on {len(faces)} samples across {len(set(ids))} user(s).")
    print(f"Saved to {config.MODEL_PATH}")


if __name__ == "__main__":
    train()
