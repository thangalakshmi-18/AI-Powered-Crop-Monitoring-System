import os
import json
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# ── Paths ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "datasets", "crop_images")
MODEL_PATH = os.path.join(BASE_DIR, "models", "crop_disease_model.h5")
LABELS_PATH = os.path.join(BASE_DIR, "models", "crop_labels.json")

IMG_SIZE = (224, 224)
BATCH_SIZE = 16
EPOCHS = 5

# ── Load dataset ──────────────────────────────────────
print("Loading dataset...")

datagen = ImageDataGenerator(
    rescale=1.0 / 255,
    validation_split=0.2,
    horizontal_flip=True,
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

# ── Save labels ───────────────────────────────────────
labels = {v: k for k, v in train_data.class_indices.items()}
with open(LABELS_PATH, "w") as f:
    json.dump(labels, f)

print("Classes:", list(train_data.class_indices.keys()))

# ── Model ─────────────────────────────────────────────
base_model = MobileNetV2(
    input_shape=(224, 224, 3),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

x = base_model.output
x = GlobalAveragePooling2D()(x)
x = Dropout(0.3)(x)
x = Dense(128, activation="relu")(x)
output = Dense(len(labels), activation="softmax")(x)

model = Model(inputs=base_model.input, outputs=output)

# ── Compile ───────────────────────────────────────────
model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)

print("Model ready!")

# ── Train ─────────────────────────────────────────────
history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS
)

# ── Save model ────────────────────────────────────────
model.save(MODEL_PATH)

print("Model saved at:", MODEL_PATH)

print("Final accuracy:", history.history["val_accuracy"][-1])