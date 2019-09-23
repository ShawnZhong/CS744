from pyspark import SparkContext, SparkConf 

input_path = "hdfs://clnodevm053-1.clemson.cloudlab.us:9000/web-BerkStan.txt"

# set SparkConf and SparkContext
conf = SparkConf().setAppName("a1p3")
sc = SparkContext(conf=conf)

# Read the file as RDD
lines = sc.textFile(input_path)

# Parse each line to a pair (from_node_id, to_node_id)
pairs = lines.filter(lambda l: l[0] != "#")\
             .map(lambda l: l.split())

# buckets is a list of tuples (from_id, [to_id_1, to_id_2, to_id_3, ...])
buckets = pairs.groupByKey().cache()

# Set initial rank of each page to be 1.
# rank is a list of tuples (from_id, rank)
rank = buckets.mapValues(lambda e: 1.0)

# On each iteration, each page contributes to its neighbors by rank(p)/ # of neighbors.
def compute_contribution(to_id_list, rank):
    return [(to_id, rank / len(to_id_list)) for to_id in to_id_list]

for i in range(1):
    # out_edge_ranks is a list of tuples (from_id, ([to_id_1, to_id_2, to_id_3, ...], rank_for_from_id))
    out_edge_ranks = buckets.join(rank)

    # contrib is a list of tuples (to_id, contrib)
    contrib = out_edge_ranks.flatMap(lambda e: compute_contribution(e[1][0], e[1][1]))\
                            .reduceByKey(lambda e1, e2: e1 + e2)

    print(contrib.take(10))

    # Update each page's rank to be 0.15 + 0.85 * (sum of contributions).
    rank = contrib.mapValues(lambda l: 0.15 + 0.85 * l)

rank.saveAsTextFile("output")