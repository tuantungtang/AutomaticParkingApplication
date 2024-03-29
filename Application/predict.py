import os

os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import keras
import keras_preprocessing
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
from keras.models import *
from keras_preprocessing import image
from keras_preprocessing.image import ImageDataGenerator
from PIL import Image


def predict_model():
    model = load_model(r'C:\TensorFlow\TensorFlow\TVT\rps.keras')
    img = tf.keras.preprocessing.image.load_img(r"test\type_temp.jpg", target_size=(150, 150))
    ip = tf.keras.preprocessing.image.img_to_array(img)
    ip = np.array([ip])
    ip = ip.astype('float32') / 255
    prediction = model.predict(ip)
    print(prediction)
    predict_class = np.argmax(prediction, axis=-1)

    if predict_class == 0:
        return "cub"
    elif predict_class == 1:
        return "ab"
    else:
        return "exiter"


if __name__ == '__main__':
    print(predict_model())
