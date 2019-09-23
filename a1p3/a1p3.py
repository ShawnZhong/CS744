# Example scala code:

# # Load graph as an RDD of (URL, outlinks) pairs
# val links = spark.textFile(...).map(...).persist()
# var ranks = // RDD of (URL, rank) pairs
# for (i <- 1 to ITERATIONS) {
#     # Build an RDD of (targetURL, float) pairs with the contributions sent by each page
#     val contribs = links.join(ranks).flatMap {
#         (url, (links, rank)) => links.map(dest => (dest, rank/links.size))
#     }
#     # Sum contributions by URL and get new ranks
#     ranks = contribs.reduceByKey((x,y) => x+y).mapValues(sum => a/N + (1-a)*sum)
# }


import sys

from pyspark import SparkContext, SparkConf 

input_path = "hdfs://clnodevm053-1.clemson.cloudlab.us:9000/web-BerkStan.txt"

# set SparkConf and SparkContext
conf = SparkConf().setAppName("a1p3").setMaster("local")
sc = SparkContext(conf=conf)

# Read the file as RDD
lines = sc.textFile(input_path)

# Take lines from the fifth line, since the first 4 lines are comments
comments = lines.take(4)
data = lines.filter(lambda l: not l in comments)

# Parse each line to a pair (from_node_id, to_node_id)
pairs = data.map(lambda l: l.split()).groupByKey()

# For task 3
# pairs.cache()

# lines.saveAsTextFile("1.txt")