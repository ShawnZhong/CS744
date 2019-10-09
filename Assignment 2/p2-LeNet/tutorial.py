import tensorflow_datasets as tfds
import tensorflow as tf
import os
import json


os.environ["TF_CONFIG"] = json.dumps({
    "cluster": {
        "worker": [
            "node0:2222",
            "node1:2222",
            "node2:2222"
        ]
    },
    "task": {
        "index": 0,
        "type": "worker"
    }
})

strategy = tf.distribute.experimental.MultiWorkerMirroredStrategy()

# print(strategy.scope())


# """## Download the dataset

# Download the MNIST dataset and load it from [TensorFlow Datasets](https://www.tensorflow.org/datasets). This returns a dataset in `tf.data` format.

# Setting `with_info` to `True` includes the metadata for the entire dataset, which is being saved here to `info`.
# Among other things, this metadata object includes the number of train and test examples.
# """

# datasets, info = tfds.load(name='mnist', with_info=True, as_supervised=True)

# mnist_train, mnist_test = datasets['train'], datasets['test']

# """## Define distribution strategy

# Create a `MirroredStrategy` object. This will handle distribution, and provides a context manager (`tf.distribute.MirroredStrategy.scope`) to build your model inside.
# """


# """## Setup input pipeline

# When training a model with multiple GPUs, you can use the extra computing power effectively by increasing the batch size. In general, use the largest batch size that fits the GPU memory, and tune the learning rate accordingly.
# """

# # You can also do info.splits.total_num_examples to get the total
# # number of examples in the dataset.

# num_train_examples = info.splits['train'].num_examples
# num_test_examples = info.splits['test'].num_examples

# BUFFER_SIZE = 10000

# BATCH_SIZE_PER_REPLICA = 64
# BATCH_SIZE = BATCH_SIZE_PER_REPLICA * strategy.num_replicas_in_sync

# """Pixel values, which are 0-255, [have to be normalized to the 0-1 range](https://en.wikipedia.org/wiki/Feature_scaling). Define this scale in a function."""


# def scale(image, label):
#     image = tf.cast(image, tf.float32)
#     image /= 255

#     return image, label


# """Apply this function to the training and test data, shuffle the training data, and [batch it for training](https://www.tensorflow.org/api_docs/python/tf/data/Dataset#batch). Notice we are also keeping an in-memory cache of the training data to improve performance."""

# train_dataset = mnist_train.map(scale).cache().shuffle(
#     BUFFER_SIZE).batch(BATCH_SIZE)
# eval_dataset = mnist_test.map(scale).batch(BATCH_SIZE)

# """## Create the model

# Create and compile the Keras model in the context of `strategy.scope`.
# """

# with strategy.scope():
#     model = tf.keras.Sequential([
#         tf.keras.layers.Conv2D(32, 3, activation='relu',
#                                input_shape=(28, 28, 1)),
#         tf.keras.layers.MaxPooling2D(),
#         tf.keras.layers.Flatten(),
#         tf.keras.layers.Dense(64, activation='relu'),
#         tf.keras.layers.Dense(10, activation='softmax')
#     ])

#     model.compile(loss='sparse_categorical_crossentropy',
#                   optimizer=tf.keras.optimizers.Adam(),
#                   metrics=['accuracy'])

# """## Define the callbacks

# The callbacks used here are:

# *   *TensorBoard*: This callback writes a log for TensorBoard which allows you to visualize the graphs.
# *   *Model Checkpoint*: This callback saves the model after every epoch.
# *   *Learning Rate Scheduler*: Using this callback, you can schedule the learning rate to change after every epoch/batch.

# For illustrative purposes, add a print callback to display the *learning rate* in the notebook.
# """

# # Define the checkpoint directory to store the checkpoints

# checkpoint_dir = './training_checkpoints'
# # Name of the checkpoint files
# checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}")

# # Function for decaying the learning rate.
# # You can define any decay function you need.


# def decay(epoch):
#     if epoch < 3:
#         return 1e-3
#     elif epoch >= 3 and epoch < 7:
#         return 1e-4
#     else:
#         return 1e-5

# # Callback for printing the LR at the end of each epoch.


# class PrintLR(tf.keras.callbacks.Callback):
#     def on_epoch_end(self, epoch, logs=None):
#         print('\nLearning rate for epoch {} is {}'.format(epoch + 1,
#                                                           model.optimizer.lr.numpy()))


# callbacks = [
#     tf.keras.callbacks.TensorBoard(log_dir='./logs'),
#     tf.keras.callbacks.ModelCheckpoint(filepath=checkpoint_prefix,
#                                        save_weights_only=True),
#     tf.keras.callbacks.LearningRateScheduler(decay),
#     PrintLR()
# ]

# """## Train and evaluate

# Now, train the model in the usual way, calling `fit` on the model and passing in the dataset created at the beginning of the tutorial. This step is the same whether you are distributing the training or not.
# """

# model.fit(train_dataset, epochs=1, callbacks=callbacks)

# """As you can see below, the checkpoints are getting saved."""


# """To see how the model perform, load the latest checkpoint and call `evaluate` on the test data.

# Call `evaluate` as before using appropriate datasets.
# """

# model.load_weights(tf.train.latest_checkpoint(checkpoint_dir))

# eval_loss, eval_acc = model.evaluate(eval_dataset)

# print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))

# """To see the output, you can download and view the TensorBoard logs at the terminal.

# ```
# $ tensorboard --logdir=path/to/log-directory
# ```
# """

# """## Export to SavedModel

# Export the graph and the variables to the platform-agnostic SavedModel format. After your model is saved, you can load it with or without the scope.
# """

# path = 'saved_model/'

# model.save(path, save_format='tf')

# """Load the model without `strategy.scope`."""

# unreplicated_model = tf.keras.models.load_model(path)

# unreplicated_model.compile(
#     loss='sparse_categorical_crossentropy',
#     optimizer=tf.keras.optimizers.Adam(),
#     metrics=['accuracy'])

# eval_loss, eval_acc = unreplicated_model.evaluate(eval_dataset)

# print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))

# """Load the model with `strategy.scope`."""

# with strategy.scope():
#     replicated_model = tf.keras.models.load_model(path)
#     replicated_model.compile(loss='sparse_categorical_crossentropy',
#                              optimizer=tf.keras.optimizers.Adam(),
#                              metrics=['accuracy'])

#     eval_loss, eval_acc = replicated_model.evaluate(eval_dataset)
#     print('Eval loss: {}, Eval Accuracy: {}'.format(eval_loss, eval_acc))

# """### Examples and Tutorials
# Here are some examples for using distribution strategy with keras fit/compile:
# 1. [Transformer](https://github.com/tensorflow/models/blob/master/official/transformer/v2/transformer_main.py) example trained using `tf.distribute.MirroredStrategy`
# 2. [NCF](https://github.com/tensorflow/models/blob/master/official/recommendation/ncf_keras_main.py) example trained using `tf.distribute.MirroredStrategy`.

# More examples listed in the [Distribution strategy guide](../../guide/distributed_training.ipynb#examples_and_tutorials)

# ## Next steps

# * Read the [distribution strategy guide](../../guide/distributed_training.ipynb).
# * Read the [Distributed Training with Custom Training Loops](training_loops.ipynb) tutorial.

# Note: `tf.distribute.Strategy` is actively under development and we will be adding more examples and tutorials in the near future. Please give it a try. We welcome your feedback via [issues on GitHub](https://github.com/tensorflow/tensorflow/issues/new).
# """
