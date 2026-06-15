import os
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator
import json

# ── Settings ──────────────────────────────────────────────────────────────────
BASE_DIR    = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR    = os.path.join(BASE_DIR, "datasets", "crop_images")
MODEL_PATH  = os.path.join(BASE_DIR, "models", "crop_disease_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "models", "crop_labels.json")

IMG_SIZE    = (224, 224)   # MobileNetV2 expects 224x224
BATCH_SIZE  = 16
EPOCHS      = 5            # 5 epochs is enough for a good result

# ── Step 1: Load and prepare images ──────────────────────────────────────────
print("Loading images from dataset...")

datagen = ImageDataGenerator(
    rescale=1.0 / 255,        # normalize pixel values 0-1
    validation_split=0.2,     # 80% train, 20% test
    horizontal_flip=True,     # random flip for variety
    zoom_range=0.2
)

train_data = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="training"
)

val_data = datagen.flow_from_directory(
    DATA_DIR,
    target_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    class_mode="categorical",
    subset="validation"
)

# ── Step 2: Save class labels ─────────────────────────────────────────────────
# This maps numbers back to class names e.g. {0: "Tomato___Early_blight"}
labels = {v: k for k, v in train_data.class_indices.items()}
with open(LABELS_PATH, "w") as f:
    json.dump(labels, f)
print(f"Classes found: {list(train_data.class_indices.keys())}")

# ── Step 3: Load pretrained MobileNetV2 ──────────────────────────────────────
# include_top=False means we remove the last layer and add our own
print("\nLoading pretrained MobileNetV2...")
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"         # pretrained on 1 million images
)
base_model.trainable = False   # freeze the base — we only train our top layers

# ── Step 4: Add our custom classification layers ──────────────────────────────
x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation="relu")(x)
predictions = Dense(len(labels), activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=predictions)

# ── Step 5: Compile the model ─────────────────────────────────────────────────
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)
print("Model compiled successfully!")
print(f"Total classes: {len(labels)}")

# ── Step 6: Train ─────────────────────────────────────────────────────────────
print(f"\nTraining for {EPOCHS} epochs...")
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ── Step 7: Save the model ────────────────────────────────────────────────────
model.save(MODEL_PATH)
print(f"\nModel saved at: {MODEL_PATH}")
print(f"Labels saved at: {LABELS_PATH}")

final_acc = history.history["val_accuracy"][-1]
print(f"\nFinal validation accuracy: {final_acc * 100:.1f}%")
print("Done! Crop disease model is ready.")