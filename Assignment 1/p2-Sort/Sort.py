import sys

from pyspark import SparkContext, SparkConf 

# sanity check for invalid arguments
if len(sys.argv) != 3: 
    print("Usage: ./a1p2.py [input file path] [output file path]")
    exit()

# declare input and out path
input_path = sys.argv[1]
output_path = sys.argv[2]

# set SparkConf and SparkContext
conf = SparkConf().setAppName("a1p2").setMaster("local")
sc = SparkContext(conf=conf)

# parse the input file to RDD and split by comma 
lines = sc.textFile(input_path)
parts = lines.map(lambda l: l.split(","))

# sort by the country code alphabetically first and then by the timestamp 
result = parts.sortBy(lambda e: e[2], lambda e : e[-1])

# format the sorted result to csv file 
lines = result.map(lambda l: ','.join(str(e) for e in l))
lines.repartition(1).saveAsTextFile(output_path)
