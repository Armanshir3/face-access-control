"""Enroll a new user by capturing labelled face samples from a webcam."""

import json
import os
import sys

import cv2

from . import config


def load_labels():
    if os.path.isfile(config.LABELS_PATH):
        with open(config.LABELS_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_labels(labels):
    with open(config.LABELS_PATH, "w", encoding="utf-8") as f:
        json.dump(labels, f, ensure_ascii=False, indent=2)


def next_user_id(labels):
    if not labels:
        return 1
    return max(int(user_id) for user_id in labels.keys()) + 1


def capture_user(name):
    """Capture SAMPLES_PER_USER face crops for a new user and store them on disk."""
    labels = load_labels()
    user_id = next_user_id(labels)

    user_dir = os.path.join(config.DATA_DIR, str(user_id))
    os.makedirs(user_dir, exist_ok=True)

    detector = cv2.CascadeClassifier(config.CASCADE_PATH)
    camera = cv2.VideoCapture(config.CAMERA_INDEX)

    if not camera.isOpened():
        print("Error: could not access the camera.")
        return

    print(f"Enrolling '{name}' as user id {user_id}. Look at the camera.")
    count = 0

    while count < config.SAMPLES_PER_USER:
        ok, frame = camera.read()
        if not ok:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(
            gray,
            scaleFactor=config.DETECTION_SCALE_FACTOR,
            minNeighbors=config.DETECTION_MIN_NEIGHBORS,
            minSize=config.DETECTION_MIN_SIZE,
        )

        for (x, y, w, h) in faces:
            count += 1
            face_crop = cv2.resize(gray[y:y + h, x:x + w], config.FACE_SIZE)
            sample_path = os.path.join(user_dir, f"{count}.jpg")
            cv2.imwrite(sample_path, face_crop)

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(
                frame,
                f"Samples: {count}/{config.SAMPLES_PER_USER}",
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2,
            )
            break

        cv2.imshow("Enrollment - press q to cancel", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()

    if count == 0:
        print("No face captured. Enrollment aborted.")
        os.rmdir(user_dir)
        return

    labels[str(user_id)] = name
    save_labels(labels)
    print(f"Enrollment complete: {count} samples saved for '{name}'.")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m src.capture_faces <name>")
        sys.exit(1)
    capture_user(" ".join(sys.argv[1:]))
