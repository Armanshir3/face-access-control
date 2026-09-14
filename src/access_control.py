"""Real-time face detection and recognition loop that grants or denies access."""

import json
import os
import time

import cv2

from . import config
from .logger_utils import log_access


def load_labels():
    if not os.path.isfile(config.LABELS_PATH):
        return {}
    with open(config.LABELS_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def grant_access(name):
    """Hook for real hardware integration (relay, electric lock, buzzer, and so on)."""
    print(f"ACCESS GRANTED: {name}")


def deny_access():
    """Hook for a denied attempt (alarm, alert, and so on)."""
    print("ACCESS DENIED")


def run():
    if not os.path.isfile(config.MODEL_PATH):
        print("No trained model found. Run capture_faces.py then train_model.py first.")
        return

    labels = load_labels()

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(config.MODEL_PATH)

    detector = cv2.CascadeClassifier(config.CASCADE_PATH)
    camera = cv2.VideoCapture(config.CAMERA_INDEX)

    if not camera.isOpened():
        print("Error: could not access the camera.")
        return

    last_log_time = {}
    log_cooldown_seconds = 5

    print("Access control running. Press q to quit.")

    while True:
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
            face_crop = cv2.resize(gray[y:y + h, x:x + w], config.FACE_SIZE)
            user_id, confidence = recognizer.predict(face_crop)

            name = labels.get(str(user_id), "Unknown")
            recognized = confidence <= config.CONFIDENCE_THRESHOLD and name != "Unknown"

            box_color = (0, 255, 0) if recognized else (0, 0, 255)
            label = f"{name} ({confidence:.0f})" if recognized else f"Unknown ({confidence:.0f})"

            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            cv2.putText(
                frame,
                label,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                box_color,
                2,
            )

            now = time.time()
            key = name if recognized else "unknown"
            if now - last_log_time.get(key, 0) > log_cooldown_seconds:
                last_log_time[key] = now
                if recognized:
                    grant_access(name)
                    log_access(name, "GRANTED", confidence)
                else:
                    deny_access()
                    log_access("Unknown", "DENIED", confidence)

        cv2.imshow("Access Control - press q to quit", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
