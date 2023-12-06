from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json
from pyspark.sql.types import StringType, StructType, StructField
from textblob import TextBlob

# Your existing code and function definitions...



def sentiment_analysis(text):
    """ Simple sentiment analysis function using TextBlob. """
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'
    
def write_mongo(df, epoch_id):
    # Replace with your MongoDB details
    mongo_uri = "mongodb://localhost:27017/twitter_data.SentimentalAnalysis"
    df.write.format("mongo").mode("append").option("uri", mongo_uri).save()

spark = SparkSession.builder \
    .appName("MongoDBIntegration") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/twitter_data.SentimentalAnalysis") \
    .getOrCreate()

# Define UDF for sentiment analysis
sentiment_udf = udf(sentiment_analysis, StringType())
# Define the schema for the JSON data
json_schema = StructType([
    StructField("tweet_id", StringType(), True),
    StructField("entity", StringType(), True),
    StructField("tweet_content", StringType(), True)
])

# Read data from Kafka and parse the JSON data
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "localhost:9092") \
    .option("subscribe", "twitter_data") \
    .load()

df = df.selectExpr("CAST(value AS STRING)")
df = df.withColumn("jsonData", from_json(col("value"), json_schema)).select("jsonData.*")

# Perform sentiment analysis
df_with_sentiment = df.withColumn("sentiment", sentiment_udf(col("tweet_content")))

# Select relevant columns (e.g., tweet_id and sentiment)
output_df = df_with_sentiment.selectExpr("CAST(tweet_id AS STRING) as key", "to_json(struct(*)) as value")

# Write to Kafka
query = output_df.writeStream \
    .foreachBatch(write_mongo) \
    .start()

query.awaitTermination()