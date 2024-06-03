#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 27 17:00:22 2023

@author: joonjung
"""

import tensorflow as tf

from tensorflow.keras.models import Sequential

from tensorflow.keras.layers import Dense, Conv2D, MaxPool2D, BatchNormalization, Dropout, Flatten, LeakyReLU

from tensorflow.keras.losses import categorical_crossentropy

from tensorflow.keras.losses import sparse_categorical_crossentropy

from tensorflow.keras.optimizers import Adam

from tensorflow.keras.utils import to_categorical

import matplotlib.pyplot as plt

# Loading in the fashion data set
mnist = tf.keras.datasets.fashion_mnist
(train_images, train_labels), (test_images, test_labels) = mnist.load_data()

train_images = train_images.reshape(60000, 28, 28, 1)
test_images = test_images.reshape(10000, 28, 28, 1)
train_images, test_images = train_images/255, test_images/255

# Let's do some DATA AUGMENTATION

# =============================================================================
# # HSV 
# import cv2
# # from PIL import Image
# import numpy as np
# 
# gfx=[]   # to hold the HSV image array
# 
# for i in np.arange(0, 100, 1):
#     a = cv2.cvtColor(train_images[i], cv2.COLOR_BGR2HSV)
#     gfx.append(a)
# 
# gfx = np.array(gfx)
# train_images_HSV = gfx
# 
# gfx_test=[]   # to hold the HSV image array
# 
# for i in np.arange(0, 100, 1):
# 
#   b = cv2.cvtColor(test_images[i], cv2.COLOR_BGR2HSV)
#   
#   gfx_test.append(b)
# 
# gfx = np.array(gfx_test)
# test_images_HSV = gfx
# # it becomes tuple, can't work with those later
# 
# =============================================================================


# image generator for normal images 
X_train = train_images
y_train = train_labels
X_val = test_images
y_val = test_labels

from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Using ImageDataGenerator to generate images
train_datagen = ImageDataGenerator(horizontal_flip = True, 
                                  zoom_range = 0.5, rotation_range = 30)

val_datagen  = ImageDataGenerator()

# Flowing training images using train_datagen generator
train_generator = train_datagen.flow(x = X_train, y = y_train, batch_size = 64, seed = 42, shuffle = True)
# Flowing validation images using val_datagen generator
val_generator =  val_datagen.flow(x = X_val, y = y_val, batch_size = 64, seed = 42, shuffle = True)
# =============================================================================
# running the data augmented images 
# history3 = cnn_model_class.fit(train_generator, validation_data = val_generator,batch_size = 32, epochs = 20, verbose = 1)


# =============================================================================





# Baseline model from class
cnn_model_class = tf.keras.Sequential([
tf.keras.layers.Conv2D(32, (3,3), activation='relu', input_shape=(28,28,1)),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.25),
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(128, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(10, activation='softmax')
])

# To show the layers in Jupyter notebook

# model_class = cnn_model_class()
# model_class.summary()


# Fitting the model
cnn_model_class.compile(loss = 'sparse_categorical_crossentropy', optimizer = tf.keras.optimizers.Adam(0.001), metrics = ['accuracy'])    

history_model_class = cnn_model_class.fit(train_images, train_labels, batch_size = 32, verbose = 1, epochs = 20, validation_data=(test_images, test_labels))



# =============================================================================
# # Plotting the accuracies
# dict_hist = history_model_class.history
# list_ep = [i for i in range(1, 21)]
# plt.figure(figsize = (8, 8))
# plt.plot(list_ep, dict_hist['accuracy'], ls = '--', label = 'accuracy')
# plt.plot(list_ep, dict_hist['val_accuracy'], ls = '--', label = 'val_accuracy')
# plt.ylabel('Accuracy')
# plt.xlabel('Epochs')
# plt.legend()
# plt.show()
# 
# =============================================================================

# Using Dropout layers
cnn_model1 = tf.keras.Sequential([
tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(28,28,1)),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.25),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.25),
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(10, activation='softmax')
])

# Fitting the model
cnn_model1.compile(loss = 'sparse_categorical_crossentropy', optimizer = tf.keras.optimizers.Adam(0.001), metrics = ['accuracy'])    
history_model_class = cnn_model1.fit(train_images, train_labels, batch_size = 32, verbose = 1, epochs = 20, validation_data=(test_images, test_labels))


# Using Batchnormalization layers
cnn_model2 = tf.keras.Sequential([
tf.keras.layers.Conv2D(64, (3,3), activation='relu', input_shape=(28,28,1)),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.Flatten(),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dense(10, activation='softmax')
])

# Fitting the model
cnn_model2.compile(loss = 'sparse_categorical_crossentropy', optimizer = tf.keras.optimizers.Adam(0.001), metrics = ['accuracy'])    
history_model_class = cnn_model2.fit(train_images, train_labels, batch_size = 32, verbose = 1, epochs = 20, validation_data=(test_images, test_labels))

from tensorflow.keras import backend
backend.clear_session()

# from ddrop.layers import DropConnect, x = DropConnect(Dense(64, activation='relu'), prob=0.5)(x)


# Using Dropout layers, and more filters
cnn_model3 = tf.keras.Sequential([
tf.keras.layers.Conv2D(128, (3,3), activation='relu', input_shape=(28,28,1)),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.25),


tf.keras.layers.Flatten(),

tf.keras.layers.Dense(512, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(32, activation='relu'),
tf.keras.layers.Dropout(0.25),
tf.keras.layers.Dense(10, activation='softmax')
])

# Fitting the model
cnn_model3.compile(loss = 'sparse_categorical_crossentropy', optimizer = tf.keras.optimizers.Adam(0.001), metrics = ['accuracy'])    
# on normal image dataset
history_model_class = cnn_model3.fit(train_images, train_labels, batch_size = 32, verbose = 1, epochs = 20, validation_data=(test_images, test_labels))
# Epoch 20/20
# 1875/1875 [==============================] - 7s 4ms/step - loss: 0.0999 - accuracy: 0.9656 - val_loss: 0.2350 - val_accuracy: 0.9329


# on augmented data set
history3 = cnn_model3.fit(train_generator, validation_data = val_generator,batch_size = 32, epochs = 20, verbose = 1)
# Epoch 20/20
# 750/750 [==============================] - 8s 11ms/step - loss: 0.4361 - accuracy: 0.8450 - val_loss: 0.3846 - val_accuracy: 0.8724


# Playing around, drop connection instead of dropout?

# from ddrop.layers import DropConnect

# x = DropConnect(Dense(64, activation='relu'), prob=0.5)(x)

cnn_model4 = tf.keras.Sequential([
tf.keras.layers.Conv2D(512, (3,3), input_shape=(28,28,1)),
tf.keras.layers.LeakyReLU(),
tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),   
tf.keras.layers.Dropout(0.5), 
tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),    
tf.keras.layers.Dropout(0.5), 
tf.keras.layers.Conv2D(256, (3,3), activation='relu'), 
tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.Dropout(0.5), 
tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),   
tf.keras.layers.Dropout(0.3), 
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.3),


tf.keras.layers.Flatten(),

tf.keras.layers.Dense(1048, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(512, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(10, activation='softmax')
])

# Fitting the model
adam = tf.keras.optimizers.legacy.Adam(learning_rate=0.001, decay=1e-6)
cnn_model4.compile(loss = 'sparse_categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])    
# on normal image dataset
history_model_class = cnn_model4.fit(train_images, train_labels, batch_size = 32, verbose = 1, epochs = 20, validation_data=(test_images, test_labels))

#Epoch 20/20
#1875/1875 [==============================] - 22s 12ms/step - loss: 0.0284 - accuracy: 0.9898 - val_loss: 0.3078 - val_accuracy: 0.9398
# on augmented data set

history4 = cnn_model4.fit(train_generator, validation_data = val_generator,batch_size = 32, epochs = 20, verbose = 1)


# for model 5, I was playing around with batch size, and I had to optimize the model and make it not too massive like previous one, because it takes so long

cnn_model5 = tf.keras.Sequential([
tf.keras.layers.Conv2D(512, (3,3), input_shape=(28,28,1)),
tf.keras.layers.LeakyReLU(),
tf.keras.layers.Conv2D(512, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),   
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.5), 
tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
tf.keras.layers.Conv2D(256, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),  
tf.keras.layers.MaxPooling2D(2,2),  
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
tf.keras.layers.Conv2D(128, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(), 
tf.keras.layers.MaxPooling2D(2,2),   
tf.keras.layers.Dropout(0.5), 
tf.keras.layers.Conv2D(64, (3,3), activation='relu'), 
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),    
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
tf.keras.layers.BatchNormalization(),    
tf.keras.layers.MaxPooling2D(2,2),
tf.keras.layers.Dropout(0.3),

tf.keras.layers.Flatten(),

tf.keras.layers.Dense(1024, activation='relu'),
tf.keras.layers.Dropout(0.7),
tf.keras.layers.Dense(512, activation='relu'),
tf.keras.layers.Dropout(0.7),
tf.keras.layers.Dense(256, activation='relu'),
tf.keras.layers.Dropout(0.7),
tf.keras.layers.Dense(128, activation='relu'),
tf.keras.layers.Dropout(0.7),
tf.keras.layers.Dense(64, activation='relu'),
tf.keras.layers.Dropout(0.7),
tf.keras.layers.Dense(32, activation='relu'),
tf.keras.layers.Dropout(0.7),
tf.keras.layers.Dense(16, activation='relu'),
tf.keras.layers.Dropout(0.5),
tf.keras.layers.Dense(10, activation='softmax')
])

# Fitting the model
adam = tf.keras.optimizers.legacy.Adam(learning_rate=0.0001, decay=1e-6)
cnn_model5.compile(loss = 'sparse_categorical_crossentropy', optimizer = adam, metrics = ['accuracy'])    
# on normal image dataset
history_model_class = cnn_model5.fit(train_images, train_labels, batch_size = 1024, verbose = 1, epochs = 30, validation_data=(test_images, test_labels))
#Epoch 20/20
#59/59 [==============================] - 45s 764ms/step - loss: 0.2397 - accuracy: 0.9122 - val_loss: 0.2528 - val_accuracy: 0.9095

history5 = cnn_model5.fit(train_generator, validation_data = val_generator,batch_size = 1024, epochs = 30, verbose = 1)

