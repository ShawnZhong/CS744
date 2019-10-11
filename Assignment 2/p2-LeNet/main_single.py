import tensorflow as tf

# Hyperparameters and constants
batch_size = 100
num_classes = 10
epochs = 50
img_rows, img_cols = 28, 28

# Import mnist data, and seperate train and test sets
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Reshape and normalize data to match the expected input
x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
input_shape = (img_rows, img_cols, 1)
x_train, x_test = x_train / 255.0, x_test / 255.0

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
)

# Training
model.fit(
    x_train,
    y_train,
    batch_size=batch_size,
    epochs=epochs,
    validation_data=(x_test, y_test),
    callbacks=[tensorboard_callback],
)
