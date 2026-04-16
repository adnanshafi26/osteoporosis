import os
import tensorflow as tf

def inspect_model(path):
    if not os.path.exists(path):
        print(f"Model {path} not found.")
        return
    
    try:
        model = tf.keras.models.load_model(path)
        print(f"Model: {path}")
        print("Inputs:", model.input_shape)
        print("Outputs:", model.output_names if hasattr(model, 'output_names') else "N/A")
        print("Output Shape:", model.output_shape)
    except Exception as e:
        print(f"Failed to load {path}: {e}")

if __name__ == "__main__":
    os.chdir("backend")
    inspect_model("model/osteoporosis_xray_model.h5")
    inspect_model("model/osteoporosis_model.h5")
