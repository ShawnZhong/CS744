import tensorflow as tf
import os
import json
import sys

total_workers = int(sys.argv[1])
worker_index = int(sys.argv[2])

# Set up environment
os.environ["TF_CONFIG"] = json.dumps({
    "cluster": {
        "worker": [
            "node0:2222",
            "node1:2222",
            "node2:2222",
        ][:total_workers]
    },
    "task": {
        "index": worker_index,
        "type": "worker"
    }
})

# Hyperparameters and constants
# batch_size = 50
# batch_size = 100
batch_size = 200
num_classes = 10
epochs = 30
img_rows, img_cols = 28, 28


# Import mnist data, and seperate train and test sets
mnist = tf.keras.datasets.mnist
(x_train, y_train), (x_test, y_test) = mnist.load_data()

# Reshape and normalize data to match the expected input
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)
x_train, x_test = x_train / 255.0, x_test / 255.0

# Using MultiWorkerMirroredStrategy for parallel training
strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()
with strategy.scope():
    # Present summary in TensorBorad
    tensorboard_callback = tf.keras.callbacks.TensorBoard(log_dir="summary")

    # LeNet model
    model = tf.keras.Sequential([
        tf.keras.layers.Conv2D(
            32,
            kernel_size=(3, 3),
            activation='relu',
            input_shape=input_shape
        ),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Conv2D(16, kernel_size=(5, 5), activation='relu'),
        tf.keras.layers.AveragePooling2D(pool_size=(2, 2), strides=(2, 2)),
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(120, activation='relu'),
        tf.keras.layers.Dense(84, activation='relu'),
        tf.keras.layers.Dense(num_classes, activation='softmax'),
    ])

    # Model is trained using cross entropy loss and stochastic gradient descent optimizer
    model.compile(
        loss=tf.keras.losses.sparse_categorical_crossentropy,
        optimizer=tf.keras.optimizers.SGD(learning_rate=0.001),
        metrics=['accuracy'],
        callbacks=[tensorboard_callback],
    )

# Training
model.fit(
    x_train,
    y_train,
    steps_per_epoch=x_train.shape[0] // batch_size,
    # batch_size=batch_size,
    epochs=epochs,
    validation_data=(x_test, y_test),
    callbacks=[tensorboard_callback],
)

# Evaluate the accuracy and loss
score = model.evaluate(x_test, y_test)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
