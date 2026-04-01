import os
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input
from tensorflow.keras.models import Model
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.preprocessing.image import load_img, img_to_array

# Configuration
DATASET_DIR = "dataset/train"
CSV_PATH = "osteoporosis_dataset_10000_final.csv"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
EPOCHS = 10

def load_data(csv_path, dataset_dir):
    """Load labels from CSV and map to existing image files."""
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return None, None
    
    df = pd.read_csv(csv_path)
    
    # Standardize Bone Type to integers for classification
    # 1: Normal, 2: Osteopenic, 3: Osteoporotic (adjust mapping if needed)
    bone_type_map = {1: 0, 2: 1, 3: 2} # 0, 1, 2 for sparse_categorical
    df['bone_type_idx'] = df['bone_type'].map(bone_type_map)

    # Filter rows that have matching images
    valid_images = []
    bmi_labels = []
    density_labels = []
    type_labels = []

    # Check if directory exists
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir, exist_ok=True)
        print(f"Notice: {dataset_dir} was empty. Created it. Please place images named 'id.jpg' there.")
        return None, None

    for idx, row in df.iterrows():
        img_id = row['id']
        img_name = f"{img_id}.jpg"
        img_path = os.path.join(dataset_dir, img_name)
        
        if os.path.exists(img_path):
            valid_images.append(img_path)
            bmi_labels.append(row['bmi'])
            density_labels.append(row['bone_density'])
            type_labels.append(row['bone_type_idx'])

    if not valid_images:
        print("Error: No matching images found in dataset directory.")
        return None, None

    return valid_images, (np.array(bmi_labels), np.array(density_labels), np.array(type_labels))

def data_generator(image_paths, labels, batch_size):
    """Custom generator for multi-output training."""
    num_samples = len(image_paths)
    while True:
        for offset in range(0, num_samples, batch_size):
            batch_images = []
            batch_bmi = labels[0][offset:offset+batch_size]
            batch_density = labels[1][offset:offset+batch_size]
            batch_type = labels[2][offset:offset+batch_size]
            
            for i in range(offset, min(offset + batch_size, num_samples)):
                img = load_img(image_paths[i], target_size=IMG_SIZE)
                img = img_to_array(img)
                img = tf.keras.applications.mobilenet_v2.preprocess_input(img)
                batch_images.append(img)
            
            yield np.array(batch_images), {
                'bmi_output': np.array(batch_bmi),
                'density_output': np.array(batch_density),
                'type_output': np.array(batch_type)
            }

def build_multi_output_model():
    """Builds a MobileNetV2 based model with 3 output heads."""
    base_model = MobileNetV2(input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3), include_top=False, weights='imagenet')
    base_model.trainable = False

    inputs = Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.2)(x)

    # Output Heads
    bmi_output = Dense(1, name='bmi_output')(x) # Regression
    density_output = Dense(1, name='density_output')(x) # Regression
    type_output = Dense(3, activation='softmax', name='type_output')(x) # classification (3 classes)

    model = Model(inputs=inputs, outputs=[bmi_output, density_output, type_output], name="Feature_CNN")
    
    # Compile with multiple losses
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss={
            'bmi_output': 'mse',
            'density_output': 'mse',
            'type_output': 'sparse_categorical_crossentropy'
        },
        metrics={
            'bmi_output': 'mae',
            'density_output': 'mae',
            'type_output': 'accuracy'
        }
    )
    return model

def train_cnn():
    image_paths, labels = load_data(CSV_PATH, DATASET_DIR)
    
    if image_paths is None:
        print("Training aborted due to missing data.")
        return

    model = build_multi_output_model()
    print("Model built and compiled.")

    # Split data for validation
    split = int(0.8 * len(image_paths))
    train_imgs, val_imgs = image_paths[:split], image_paths[split:]
    train_labels = (labels[0][:split], labels[1][:split], labels[2][:split])
    val_labels = (labels[0][split:], labels[1][split:], labels[2][split:])

    train_gen = data_generator(train_imgs, train_labels, BATCH_SIZE)
    val_gen = data_generator(val_imgs, val_labels, BATCH_SIZE)

    steps_per_epoch = len(train_imgs) // BATCH_SIZE
    validation_steps = len(val_imgs) // BATCH_SIZE

    print("Starting Training...")
    model.fit(
        train_gen,
        steps_per_epoch=max(1, steps_per_epoch),
        validation_data=val_gen,
        validation_steps=max(1, validation_steps),
        epochs=EPOCHS
    )

    # Save the feature model
    os.makedirs("model", exist_ok=True)
    save_path = "model/feature_model.h5"
    model.save(save_path)
    print(f"Model successfully saved to {save_path}")

if __name__ == "__main__":
    train_cnn()

