"""Central configuration for the Face Recognition Access Control System."""

import os

import cv2

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
LOG_DIR = os.path.join(BASE_DIR, "logs")

MODEL_PATH = os.path.join(MODEL_DIR, "trainer.yml")
LABELS_PATH = os.path.join(MODEL_DIR, "labels.json")
ACCESS_LOG_PATH = os.path.join(LOG_DIR, "access_log.csv")

# Haar Cascade shipped with OpenCV is used for face detection.
CASCADE_PATH = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")

CAMERA_INDEX = 0
FACE_SIZE = (200, 200)
SAMPLES_PER_USER = 60

# LBPH prediction returns a distance, not a probability.
# Lower value means a closer match. Anything above this is rejected.
CONFIDENCE_THRESHOLD = 55

DETECTION_SCALE_FACTOR = 1.1
DETECTION_MIN_NEIGHBORS = 5
DETECTION_MIN_SIZE = (90, 90)

for directory in (DATA_DIR, MODEL_DIR, LOG_DIR):
    os.makedirs(directory, exist_ok=True)
