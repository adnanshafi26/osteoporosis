import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array

def preprocess_xray(image_path, target_size=(224, 224), grayscale=False):
    """
    Preprocesses an X-ray image for CNN prediction using TensorFlow/Keras.
    Loads as RGB (3 channels) by default for pretrained models like MobileNetV2, ResNet50.
    """
    color_mode = "grayscale" if grayscale else "rgb"
    
    # Load image and resize
    img = load_img(image_path, target_size=target_size, color_mode=color_mode)
    
    # Convert PIL Image to Numpy Array
    img_array = img_to_array(img)
    
    # Normalize pixel values between 0 and 1
    img_array = img_array / 255.0
    
    # Expand dimensions to add batch size: (1, 224, 224, 3)
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array