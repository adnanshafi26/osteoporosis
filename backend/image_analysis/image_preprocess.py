import cv2
import numpy as np

def preprocess_xray(image_path):

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    img = cv2.resize(img, (224,224))

    img = img / 255.0

    img = np.reshape(img, (1,224,224,1))

    return img