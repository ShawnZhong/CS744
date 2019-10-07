import tensorflow as tf
import os
import numpy as np
import time
import datetime

# define the command line flags that can be sent
tf.app.flags.DEFINE_integer("task_index", 0, "Index of task with in the job.")
tf.app.flags.DEFINE_string("job_name", "worker", "either worker or ps")
tf.app.flags.DEFINE_string("deploy_mode", "single", "either single or cluster")
tf.app.flags.DEFINE_string("batch_size", "100", "either single or cluster")
tf.app.flags.DEFINE_string("n_epochs", "6", "either single or cluster")
tf.app.flags.DEFINE_string("learning_rate", "0.01", "either single or cluster")

FLAGS = tf.app.flags.FLAGS

tf.logging.set_verbosity(tf.logging.DEBUG)

clusterSpec_single = tf.train.ClusterSpec({
    "worker": [
        "10.10.1.1:2222"
    ]
})

clusterSpec_cluster = tf.train.ClusterSpec({
    "ps": [
        "10.10.1.1:2222"
    ],
    "worker": [
        "10.10.1.1:2223",
        "10.10.1.2:2222"
    ]
})

clusterSpec_cluster2 = tf.train.ClusterSpec({
    "ps": [
        "10.10.1.1:2224"
    ],
    "worker": [
        "10.10.1.1:2225",
        "10.10.1.2:2224",
        "10.10.1.3:2224"
    ]
})

clusterSpec = {
    "single": clusterSpec_single,
    "cluster": clusterSpec_cluster,
    "cluster2": clusterSpec_cluster2
}

clusterinfo = clusterSpec[FLAGS.deploy_mode]
server = tf.train.Server(
    clusterinfo, job_name=FLAGS.job_name, task_index=FLAGS.task_index)

if FLAGS.job_name == "ps":
    server.join()
elif FLAGS.job_name == "worker":
    from tensorflow.examples.tutorials.mnist import input_data

    mnist = input_data.read_data_sets("MNIST_data/", one_hot=True)

    with tf.device(
            tf.train.replica_device_setter(worker_device="/job:worker/task:%d" % FLAGS.task_index, cluster=clusterinfo)):

        batch_size = int(FLAGS.batch_size)
        learning_rate = float(FLAGS.learning_rate)
        n_epochs = int(FLAGS.n_epochs)

        n_features = 784
        n_classes = 10

        x = tf.placeholder(dtype=tf.float32, shape=[None, n_features])
        y = tf.placeholder(dtype=tf.float32, shape=[None, n_classes])
        w = tf.Variable(tf.zeros([n_features, n_classes]))
        b = tf.Variable(tf.zeros([n_classes]))

        prediction = tf.nn.softmax(tf.matmul(x, w) + b)
        loss = tf.reduce_mean(-tf.reduce_sum(y *
                                             tf.log(prediction), reduction_indices=1))
        correct_prediction = tf.equal(
            tf.argmax(prediction, 1), tf.argmax(y, 1))
        accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))
        global_step = tf.contrib.framework.get_or_create_global_step()
        tf.summary.histogram("prediction", prediction)
        tf.summary.scalar("loss", loss)
        tf.summary.scalar("accuracy", accuracy)
        tf_summary = tf.summary.merge_all()

        optimizer = tf.train.GradientDescentOptimizer
        train_op = optimizer(learning_rate=learning_rate).minimize(loss)

        n_workers = len(vars(clusterinfo)['_cluster_spec']['worker'])
        num_curr_examples = (mnist.train.num_examples / n_workers)
        print('Number of Workers: ', n_workers)
        print('Current shrad size: ', num_curr_examples)

    init = tf.initialize_all_variables()
    with tf.Session(server.target) as sess:

        sess.run(init)
        train_writer = tf.summary.FileWriter(
            "log/asynch_%s" % (FLAGS.deploy_mode), sess.graph)
        start_time = datetime.datetime.now()
        for epoch in range(n_epochs):
            n_batches = int(mnist.train.num_examples/batch_size)

            for batch in range(n_batches):
                if batch % n_workers != FLAGS.task_index:
                  #   print('skipping this batch ', batch)
                    continue
                batch_xs, batch_ys = mnist.train.next_batch(batch_size)
                _, merged_summary = sess.run([train_op, tf_summary], feed_dict={
                                             x: batch_xs, y: batch_ys})
                train_writer.add_summary(
                    merged_summary, n_batches*epoch + batch)
            current_time = datetime.datetime.now()
            print("Epoch done:%d, accuracy: %s, time: %s" % (epoch, sess.run(accuracy, feed_dict={
                  x: mnist.test.images, y: mnist.test.labels}), str((current_time-start_time).total_seconds())))

        end_time = datetime.datetime.now()
        print("Total_time_taken:%s" %
              (str((end_time-start_time).total_seconds())))
        print("process done")
