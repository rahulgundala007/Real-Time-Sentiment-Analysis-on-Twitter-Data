from flask import Flask, render_template
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, udf, from_json
from pyspark.sql.types import StringType, StructType, StructField
from textblob import TextBlob

app = Flask(__name__)

# Initialize Spark Session
spark = SparkSession.builder \
    .appName("MongoDBIntegration") \
    .config("spark.mongodb.output.uri", "mongodb://localhost:27017/twitter_data.Project691") \
    .getOrCreate()

# Define UDF for sentiment analysis
def sentiment_analysis(text):
    analysis = TextBlob(text)
    if analysis.sentiment.polarity > 0:
        return 'Positive'
    elif analysis.sentiment.polarity == 0:
        return 'Neutral'
    else:
        return 'Negative'

sentiment_udf = udf(sentiment_analysis, StringType())

# Define the schema for the JSON data
json_schema = StructType([
    StructField("tweet_id", StringType(), True),
    StructField("entity", StringType(), True),
    StructField("tweet_content", StringType(), True)
])

# Initialize data source (empty list for now)
data_source = []

@app.route('/')
def index():
    return render_template('index.html', data=data_source)

if __name__ == '__main__':
    app.run(debug=True)
