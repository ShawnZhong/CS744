import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data

# define the command line flags that can be sent
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task with in the job.")
tf.app.flags.DEFINE_string("job_name", "worker", "either worker or ps")
tf.app.flags.DEFINE_string("deploy_mode", "single", "either single or cluster")
FLAGS = tf.app.flags.FLAGS

tf.logging.set_verbosity(tf.logging.DEBUG)

clusterSpec_single = tf.train.ClusterSpec({
    "worker": [
        "localhost:2222"
    ]
})

clusterSpec_cluster = tf.train.ClusterSpec({
    "ps": [
        "node0:2222"
    ],
    "worker": [
        "node0:2223",
        "node1:2222"
    ]
})

clusterSpec_cluster2 = tf.train.ClusterSpec({
    "ps": [
        "node0:2222"
    ],
    "worker": [
        "node0:2223",
        "node1:2222",
        "node2:2222",
    ]
})

clusterSpec = {
    "single": clusterSpec_single,
    "cluster": clusterSpec_cluster,
    "cluster2": clusterSpec_cluster2
}

clusterinfo = clusterSpec[FLAGS.deploy_mode]
server = tf.distribute.Server(
    clusterinfo,
    job_name=FLAGS.job_name,
    task_index=FLAGS.task_index
)

mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

if FLAGS.job_name == "ps":
    server.join()
elif FLAGS.job_name == "worker":
    with tf.device(
        tf.train.replica_device_setter(
            worker_device="/job:worker/task:%d" % FLAGS.task_index,
            cluster=clusterinfo
        )
    ):
        x = tf.placeholder(tf.float32, [None, 784])
        y = tf.placeholder(tf.float32, [None, 10])
        W = tf.Variable(tf.random.uniform([784, 10]))
        b = tf.Variable(tf.random.uniform([10]))

        pred = tf.nn.softmax(tf.matmul(x, W) + b)
        loss = tf.reduce_mean(-tf.reduce_sum(y * tf.log(pred),
                                             reduction_indices=1))
        optimizer = tf.train.GradientDescentOptimizer(0.01).minimize(loss)

        pred_label = tf.argmax(pred, 1)
        actual_label = tf.argmax(y, 1)
        equality = tf.equal(pred_label, actual_label)
        accuracy = tf.reduce_mean(tf.cast(equality, tf.float32))

        tf.summary.scalar("Accuracy", accuracy)
        tf.summary.scalar("Loss", loss)

        metric = tf.summary.merge_all()

    init = tf.global_variables_initializer()

    epoch = 50
    batch_size = 100

    with tf.Session(server.target) as sess:
        sess.run(init)
        writer = tf.summary.FileWriter("summary", sess.graph)

        for i in range(epoch):

            num_batch = mnist.train.num_examples // batch_size

            for j in range(num_batch):
                xs, ys = mnist.train.next_batch(batch_size)
                sess.run(optimizer, feed_dict={x: xs, y: ys})

            xs, ys = mnist.test.next_batch(batch_size)
            a, l, summary = sess.run(
                [accuracy, loss, metric], feed_dict={x: xs, y: ys})
            print("Epoch: %d, Loss: %f, Accuracy: %f" % (i, l, a))
            writer.add_summary(summary, i)

        writer.close()
