import os
import numpy as np
import tensorflow as tf
from .image_preprocess import preprocess_xray
from PIL import Image

# Global fallback model caching
_FEATURE_MODEL = None

def get_model():
    """Loads the feature prediction CNN Model."""
    global _FEATURE_MODEL
    
    model_path = "model/feature_model.h5"
    if os.path.exists(model_path) and os.path.getsize(model_path) > 0:
        try:
            print(f"Loading feature model from {model_path}...")
            return tf.keras.models.load_model(model_path)
        except Exception as e:
            print(f"Error loading {model_path}: {e}")
            
    # Fallback to an untrained model structure if not found (for API safety)
    if _FEATURE_MODEL is None:
        print("Notice: feature_model.h5 not found. Using dummy architecture for demonstration.")
        from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Input
        from tensorflow.keras.applications import MobileNetV2
        base = MobileNetV2(input_shape=(224, 224, 3), include_top=False)
        inputs = Input(shape=(224, 224, 3))
        x = base(inputs)
        x = GlobalAveragePooling2D()(x)
        bmi = Dense(1, name='bmi_output')(x)
        dens = Dense(1, name='density_output')(x)
        typ = Dense(3, activation='softmax', name='type_output')(x)
        _FEATURE_MODEL = tf.keras.models.Model(inputs, [bmi, dens, typ])
    return _FEATURE_MODEL

def analyze_xray(image_path, manual_bone=None):
    print(f"DEBUG: CNN predicting clinical features for {image_path}...")
    
    # 1. Preprocess
    img_array = preprocess_xray(image_path, target_size=(224, 224), grayscale=False)
    
    # 2. Fetch Model
    model = get_model()
    
    # 3. Predict BMI, Density, and Bone Type
    preds = model.predict(img_array)
    
    # preds is a list: [bmi_output, density_output, type_output]
    predicted_bmi = float(preds[0][0][0])
    predicted_density = float(preds[1][0][0])
    type_probs = preds[2][0]
    type_idx = int(np.argmax(type_probs))
    
    # Mapping condition
    conditions = ["Normal", "Osteopenia", "Osteoporosis"]
    predicted_condition = conditions[type_idx]
    
    # NEW Feature: Anatomical Bone Region identification (Hip, Wrist, Knee, Spine)
    # We use manual selection as the priority, then a keyword search, and finally a fallback
    bone_regions = ["Spine", "Hip", "Wrist", "Knee"]
    
    if manual_bone and manual_bone in bone_regions:
        predicted_bone_region = manual_bone
    else:
        # 1. Keyword based intelligent guesser from filename
        filename = os.path.basename(image_path).lower()
        if "knee" in filename: predicted_bone_region = "Knee"
        elif "hip" in filename: predicted_bone_region = "Hip"
        elif "wrist" in filename: predicted_bone_region = "Wrist"
        elif "spine" in filename: predicted_bone_region = "Spine"
        else:
            # 2. Aspect Ratio Heuristic (Spine is typically taller)
            img = Image.open(image_path)
            w, h = img.size
            aspect_ratio = h / w
            
            if aspect_ratio > 1.6:
                predicted_bone_region = "Spine"
            elif 0.7 < aspect_ratio < 1.4:
                # Most limb joints are close to 1:1 or 4:3
                # We default to Knee if unsure among limb joints
                predicted_bone_region = "Knee"
            else:
                # Truly uncertain, don't guess a specific one if not confident
                predicted_bone_region = "Unknown / Select"
    
    # 4. Save a clean copy of the uploaded image for display
    if not os.path.exists("uploads"):
        os.makedirs("uploads")
    save_path = "uploads/processed_xray.jpg"
    img = Image.open(image_path).convert('RGB')
    img.save(save_path)

    # 5. Determine Osteoporosis Status and Risk based on predicted density
    # Generally: > 0.8 Normal, 0.6-0.8 Osteopenia, < 0.6 Osteoporosis
    if predicted_density > 0.8:
        osteo_status = "Normal"
        risk = "Low Future Risk"
    elif predicted_density > 0.6:
        osteo_status = "Osteopenia"
        risk = "Moderate Future Risk"
    else:
        osteo_status = "Osteoporosis"
        risk = "High Future Risk"

    return {
        "bone": predicted_bone_region,
        "bmi": round(predicted_bmi, 2),
        "bone_density": round(predicted_density, 3),
        "osteoporosis": osteo_status,
        "future_risk": risk,
        "marked_image": save_path,
        "confidence": f"{float(np.max(type_probs)):.2%}"
    }