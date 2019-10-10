import tensorflow as tf
import input_data

# Disable eager execution for tensorflow 2.0
tf.compat.v1.disable_eager_execution()

# Initialize epoch and batch size
epoch = 50
batch_size = 100

# Import mnist database
mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

# Initialize placeholder for inputs and variable for parameters
x = tf.compat.v1.placeholder(tf.float32, [None, 784])
y = tf.compat.v1.placeholder(tf.float32, [None, 10])
W = tf.Variable(tf.random.uniform([784, 10]))
b = tf.Variable(tf.random.uniform([10]))

# Define a function for predictied digit
pred = tf.nn.softmax(tf.matmul(x, W) + b)

# Define loss function
loss = tf.reduce_mean(
    input_tensor=-tf.reduce_sum(
        input_tensor=y * tf.math.log(pred),
        axis=1
    )
)

# Define optimizer
optimizer = tf.compat.v1.train.GradientDescentOptimizer(0.01) \
    .minimize(loss)

# Define variables used for testing
pred_label = tf.argmax(input=pred, axis=1)
actual_label = tf.argmax(input=y, axis=1)
accuracy = tf.reduce_mean(
    input_tensor=tf.cast(tf.equal(pred_label, actual_label), tf.float32)
)

# Summary for accuracy and loss
tf.compat.v1.summary.scalar("Accuracy", accuracy)
tf.compat.v1.summary.scalar("Loss", loss)
metric = tf.compat.v1.summary.merge_all()

# Initialize global variable
init = tf.compat.v1.global_variables_initializer()

# Start the training session
with tf.compat.v1.Session() as sess:
    sess.run(init)

    # Present summary in TensorBoard
    writer = tf.compat.v1.summary.FileWriter("summary", sess.graph)

    # Iterate each epoch
    for i in range(epoch):
        num_batch = mnist.train.num_examples // batch_size
        # Iterate each batch
        for j in range(num_batch):
            x_train, y_train = mnist.train.next_batch(batch_size)
            sess.run(optimizer, feed_dict={x: x_train, y: y_train})
        x_test, y_test = mnist.test.next_batch(batch_size)
        # Evaluate the model in each epoch
        a, l, summary = sess.run(
            [accuracy, loss, metric],
            feed_dict={x: x_test, y: y_test}
        )
        print("Epoch: %d, Loss: %f, Accuracy: %f" % (i, l, a))

        # Record accuracy and loss to the summary
        writer.add_summary(summary, i)

    writer.close()
