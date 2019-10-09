import tensorflow as tf
from tensorflow.keras.layers import Dense, Dropout, Flatten, Activation, Input, AveragePooling2D, Conv2D
from tensorflow.keras import Sequential
import os
import json
import sys


# os.environ["TF_CONFIG"] = json.dumps({
#     "cluster": {
#         "worker": [
#             "node0:2222",
#             "node1:2222",
#             "node2:2222"
#         ]
#     },
#     "task": {
#         "index": int(sys.argv[1]),
#         "type": "worker"
#     }
# })

batch_size = 100
num_classes = 10
epochs = 10
img_rows, img_cols = 28, 28

# the data, split between train and test sets
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)

x_train, x_test = x_train / 255.0, x_test / 255.0

# convert class vectors to binary class matrices
y_train = tf.keras.utils.to_categorical(y_train, num_classes)
y_test = tf.keras.utils.to_categorical(y_test, num_classes)

# strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()

# with strategy.scope():
model = Sequential([
    Conv2D(32, kernel_size=(3, 3),
           activation='relu',
           input_shape=input_shape),
    AveragePooling2D(pool_size=(2, 2), strides=(2, 2)),
    Conv2D(16, kernel_size=(5, 5), activation='relu'),
    AveragePooling2D(pool_size=(2, 2), strides=(2, 2)),
    Flatten(),
    Dense(120, activation='relu'),
    Dense(84, activation='relu'),
    Dense(num_classes, activation='softmax'),
])

# model = tf.keras.Sequential([
#     tf.keras.layers.Conv2D(32, 3, activation='relu', input_shape=(28, 28, 1)),
#     tf.keras.layers.MaxPooling2D(),
#     tf.keras.layers.Flatten(),
#     tf.keras.layers.Dense(64, activation='relu'),
#     tf.keras.layers.Dense(10, activation='softmax')
# ])

model.compile(loss=tf.keras.losses.categorical_crossentropy,
              optimizer=tf.keras.optimizers.Adadelta(),
              metrics=['accuracy'])

model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          validation_data=(x_test, y_test))

score = model.evaluate(x_test, y_test)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
