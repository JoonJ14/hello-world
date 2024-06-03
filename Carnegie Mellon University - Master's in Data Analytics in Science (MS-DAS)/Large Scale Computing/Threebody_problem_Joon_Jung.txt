#Importing all the required libraries
import tensorflow as tf
import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import InputLayer,Conv2D, Conv3D,MaxPooling2D, Dense, Flatten, Dropout, BatchNormalization
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import TensorBoard
import matplotlib.pyplot as plt
from tensorflow.keras.callbacks import EarlyStopping,ReduceLROnPlateau
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

train_X_initial = pd.read_csv('~/joon/train_X.csv',header=None)

train_Y_initial = pd.read_csv('~/joon/train_Y.csv',header=None)


train_X, test_X = train_test_split(train_X_initial, test_size=0.01, random_state=14, shuffle=True)
train_Y, test_Y = train_test_split(train_Y_initial, test_size=0.01, random_state=14, shuffle=True)

#Setting a seed for analysis.

tf.keras.utils.set_random_seed(14)
tf.config.experimental.enable_op_determinism()


model = tf.keras.Sequential([
    InputLayer(input_shape = (3,)),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(128, activation='relu'),
    Dense(4, activation='linear')
])


model.compile(optimizer=tf.keras.optimizers.Adam(), loss=tf.keras.losses.MeanAbsoluteError(), metrics=['MeanAbsoluteError', 'accuracy'])


train_model = model.fit(train_X, train_Y, epochs=1000, batch_size = 5000, verbose=1, validation_data=(test_X, test_Y))

# Plotting the train and test loss
plt.plot(train_model.history['val_mean_absolute_error'], label='Val_MAE', color='red', linestyle='dashed')
plt.plot(train_model.history['mean_absolute_error'], label='Train_MAE', color='blue')
plt.yscale('log')
plt.legend()
plt.title('MAE')
plt.savefig('TrainTest.png')
plt.clf()



# Plotting the train and test accuracy
plt.plot(train_model.history['val_accuracy'], label='Val_accuracy', color='red', linestyle='dashed')
plt.plot(train_model.history['accuracy'], label='Train_accuracy', color='blue')
plt.yscale('log')
plt.legend()
plt.title('Accuracy')
plt.savefig('TrainTestaccuracy.png')
plt.clf()


# Calculating the final test accuracy
predicted_Y = model.predict(test_X)
# predicted_classes = np.argmax(predicted_classes, axis=1)

from sklearn.metrics import r2_score

score = r2_score(test_Y, predicted_Y)
print("The final test accuracy of the model is {}%".format(round(score, 2) * 100))



# scp jjung5@bridges2.psc.edu:/jet/home/jjung5/joon/TrainTest.png /Users/joonjung/Desktop/CMU/LargeScale

# scp jjung5@bridges2.psc.edu:/jet/home/jjung5/joon/TrainTestaccuracy.png /Users/joonjung/Desktop/CMU/LargeScale