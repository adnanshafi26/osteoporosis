import os
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import ModelCheckpoint, EarlyStopping, ReduceLROnPlateau

# Configuration
DATASET_DIR = "../BoneFractureDataset"
IMG_SIZE = (224, 224)
BATCH_SIZE = 32
INITIAL_EPOCHS = 5
FINE_TUNE_EPOCHS = 15

def train_fracture_model_enhanced():
    print("Initializing Data Generators...")
    
    # Advanced Data Augmentation for training
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=30,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.3,
        horizontal_flip=True,
        brightness_range=[0.8, 1.2],
        fill_mode='nearest'
    )

    test_datagen = ImageDataGenerator(rescale=1./255)

    # Load Training Data
    train_generator = train_datagen.flow_from_directory(
        os.path.join(DATASET_DIR, "training"),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary',
        shuffle=True
    )

    # Load Validation Data
    validation_generator = test_datagen.flow_from_directory(
        os.path.join(DATASET_DIR, "testing"),
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='binary'
    )

    # Build Model
    print("Building Fracture Detection Model (MobileNetV2)...")
    base_model = MobileNetV2(weights='imagenet', include_top=False, input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    
    # Phase 1: Freeze base model
    base_model.trainable = False 

    inputs = Input(shape=(IMG_SIZE[0], IMG_SIZE[1], 3))
    x = base_model(inputs, training=False)
    x = GlobalAveragePooling2D()(x)
    x = Dropout(0.3)(x) # Increased dropout for better generalization
    outputs = Dense(1, activation='sigmoid')(x)

    model = Model(inputs, outputs)

    # Compile for initial training
    model.compile(
        optimizer=Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    # Callbacks
    os.makedirs("model", exist_ok=True)
    checkpoint = ModelCheckpoint(
        "model/fracture_model.h5",
        monitor='val_accuracy',
        save_best_only=True,
        mode='max',
        verbose=1
    )
    
    early_stop = EarlyStopping(
        monitor='val_loss',
        patience=5,
        restore_best_weights=True,
        verbose=1
    )
    
    reduce_lr = ReduceLROnPlateau(
        monitor='val_loss',
        factor=0.2,
        patience=3,
        min_lr=1e-7,
        verbose=1
    )

    print("Phase 1: Training top layers...")
    model.fit(
        train_generator,
        epochs=INITIAL_EPOCHS,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stop, reduce_lr]
    )

    # Phase 2: Fine-tuning
    print("Phase 2: Fine-tuning the base model...")
    base_model.trainable = True
    
    # Fine-tune from this layer onwards
    # MobileNetV2 has 154 layers. We can freeze the first 100 and unfreeze the rest.
    fine_tune_at = 100
    for layer in base_model.layers[:fine_tune_at]:
        layer.trainable = False

    # Recompile with a much lower learning rate
    model.compile(
        optimizer=Adam(learning_rate=1e-5),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )

    total_epochs = INITIAL_EPOCHS + FINE_TUNE_EPOCHS
    
    model.fit(
        train_generator,
        epochs=total_epochs,
        initial_epoch=INITIAL_EPOCHS,
        validation_data=validation_generator,
        callbacks=[checkpoint, early_stop, reduce_lr]
    )

    print("Training finished. Final model saved to model/fracture_model.h5")

if __name__ == "__main__":
    train_fracture_model_enhanced()
