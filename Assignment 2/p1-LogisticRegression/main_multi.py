import tensorflow as tf
import input_data

# define the command line flags that can be sent
tf.compat.v1.flags.DEFINE_integer("task_index", 0, "Index of task.")
tf.compat.v1.flags.DEFINE_string("job_name", "worker", "worker or ps")
tf.compat.v1.flags.DEFINE_string("deploy_mode", "single", "single or cluster")
FLAGS = tf.compat.v1.flags.FLAGS

tf.compat.v1.logging.set_verbosity(tf.compat.v1.logging.DEBUG)
tf.compat.v1.disable_eager_execution()

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
        tf.compat.v1.train.replica_device_setter(
            worker_device="/job:worker/task:%d" % FLAGS.task_index,
            cluster=clusterinfo
        )
    ):
        x = tf.compat.v1.placeholder(tf.float32, [None, 784])
        y = tf.compat.v1.placeholder(tf.float32, [None, 10])
        W = tf.Variable(tf.random.uniform([784, 10]))
        b = tf.Variable(tf.random.uniform([10]))

        pred = tf.nn.softmax(tf.matmul(x, W) + b)
        loss = tf.reduce_mean(input_tensor=-tf.reduce_sum(input_tensor=y * tf.math.log(pred),
                                                          axis=1))
        optimizer = tf.compat.v1.train.GradientDescentOptimizer(
            0.01).minimize(loss)

        pred_label = tf.argmax(input=pred, axis=1)
        actual_label = tf.argmax(input=y, axis=1)
        equality = tf.equal(pred_label, actual_label)
        accuracy = tf.reduce_mean(input_tensor=tf.cast(equality, tf.float32))

        tf.compat.v1.summary.scalar("Accuracy", accuracy)
        tf.compat.v1.summary.scalar("Loss", loss)

        metric = tf.compat.v1.summary.merge_all()

    init = tf.compat.v1.global_variables_initializer()

    epoch = 1
    batch_size = 100

    with tf.compat.v1.Session(server.target) as sess:
        sess.run(init)
        writer = tf.compat.v1.summary.FileWriter("summary", sess.graph)

        for i in range(epoch):

            num_batch = mnist.train.num_examples // batch_size

            for j in range(num_batch):
                xs, ys = mnist.train.next_batch(batch_size)
                sess.run(optimizer, feed_dict={x: xs, y: ys})

            xs, ys = mnist.test.next_batch(batch_size)
            a, l, summary = sess.run(
                [accuracy, loss, metric],
                feed_dict={x: xs, y: ys}
            )
            print("Epoch: %d, Loss: %f, Accuracy: %f" % (i, l, a))
            writer.add_summary(summary, i)

        writer.close()
