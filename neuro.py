import tensorflow as tf
from keras import Input
from keras.src.layers import Conv2D, MaxPooling2D, Dense, Dropout, Flatten
from tensorflow import keras
import random

import numpy as np
import cv2 as cv
# Create the array of data

import os


image = cv.imread('mail_images/12447682014154883968.png')

WINDOW_SIZE = (23, )*2
OFFSET = 3

a = 1

test_path_dir = "gen_captcha/0cPY7b"


def get_size(image: np.ndarray, thresh=255):
    lw = 0
    rw = image.shape[1]

    th = 0
    bh = image.shape[0]

    while all([pixel >= thresh for pixel in image[th:][0]]):
        th += 1

    while all([pixel >= thresh for pixel in image[bh - 1:][0]]):
        bh -= 1

    while all([image[pixel, lw] >= thresh for pixel in range(image.shape[0])]):
        lw += 1

    while all([image[pixel, rw - 1] >= thresh for pixel in range(image.shape[0])]):
        rw -= 1

    return (lw, rw, th, bh)


def get_train_from_image(capcha_path_dir):
    orig, damage = os.listdir(capcha_path_dir)
    orig = cv.cvtColor(cv.imread(os.path.join(capcha_path_dir, orig)), cv.COLOR_BGR2GRAY)
    damage = cv.cvtColor(cv.imread(os.path.join(capcha_path_dir, damage)), cv.COLOR_BGR2GRAY)
    lw, rw, th, bh = get_size(orig)
    x = random.randint(lw, rw - WINDOW_SIZE[0])
    y = random.randint(th + 5, bh - WINDOW_SIZE[1] - 5)

    random_orig_crop = orig[y:y+WINDOW_SIZE[1], x:x + WINDOW_SIZE[0]]
    random_damage_crop = damage[y:y+WINDOW_SIZE[1], x:x + WINDOW_SIZE[0]]
    return random_orig_crop, random_damage_crop


orig_crop, damage_crop = get_train_from_image(test_path_dir)


def get_train_data():
    list_dirs = os.listdir("gen_captcha")
    train_data = []
    train_label = []
    for dir in list_dirs:
        orig_crop, damage_crop = get_train_from_image(os.path.join("gen_captcha", dir))
        orig_crop = orig_crop.astype(dtype="float32")
        orig_crop /= 255
        damage_crop = damage_crop.astype(dtype="float32")
        damage_crop /= 255
        train_data.append(orig_crop)
        train_label.append(damage_crop)
    return train_data, train_label

train_data, train_label = get_train_data()

# train_data = np.array(train_data)
# train_data = train_data.reshape(train_data.shape[0], 1, *WINDOW_SIZE)
train_data_np = np.asarray(train_data)
# train_label = np.array(train_label)
train_label_np = np.asarray(train_data)

### Build the model

model = keras.Sequential(
    # keras.layers.Dense(WINDOW_SIZE[0]**2, input_shape=(WINDOW_SIZE[0]**2, )),
)
model.add(Conv2D(32,(3, 3), activation = 'relu', input_shape=WINDOW_SIZE, data_format='channels_first'))
model.add(Conv2D(32,(3, 3), activation = 'relu'))
model.add(Conv2D(32, (3, 3), activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dropout(0.5))
model.add(Dense(10, activation='softmax'))

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train the model

model.fit(train_data_np, train_label_np, epochs=1000)
model.save("model.keras")
