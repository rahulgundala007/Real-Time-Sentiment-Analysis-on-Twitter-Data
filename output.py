from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf
from pyspark.sql.types import StringType
from textblob import TextBlob

def analyze_sentiment(text):
    return TextBlob(text).sentiment.polarity

def main():
    # Initialize Spark Session
    spark = SparkSession.builder \
        .appName("KafkaSentimentAnalysis") \
        .getOrCreate()

    # Define UDF for sentiment analysis
    sentiment_analysis = udf(analyze_sentiment, StringType())

    # Read from Kafka
    df = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "input_topic") \
        .load()

    # Process data
    processed_df = df.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
                     .withColumn("sentiment", sentiment_analysis(col("value")))

    # Write to Kafka
    query = processed_df.selectExpr("CAST(key AS STRING) AS key", "to_json(struct(*)) AS value") \
        .writeStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("topic", "output_topic") \
        .option("checkpointLocation", "/path/to/checkpoint/dir") \
        .start()

    query.awaitTermination()

if __name__ == "__main__":
    main()
