import sys
import os

# Add backend folder to path
sys.path.append(os.path.abspath("backend"))

from model.predict import predict_osteoporosis

features = [65,0,22,0.55,800,20]

result = predict_osteoporosis(features)

print("Prediction:", result)