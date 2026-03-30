import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "../models/osteoporosis_model.pkl")

DATASET_PATH = os.path.join(BASE_DIR, "dataset/sample_data.csv")

UPLOAD_FOLDER = os.path.join(BASE_DIR, "dataset/uploads")

ALLOWED_EXTENSIONS = {"csv"}