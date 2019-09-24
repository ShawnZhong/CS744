# Overview
This application runs the PageRank algorithm described in https://en.wikipedia.org/wiki/PageRank#Simplified_algorithm on a dataset of 2 columns, each representing where the URL is located and where the URL is pointing to, separated by a tab character. 

# Usage
To run this application, use the following

```sh
spark-submit PageRank.py
```

# Assumptions 
The machine should have Python 2.7 (with pyspark), Hadoop, and Spark installed. 
