from flask import Flask, render_template
import pandas as pd
import pymongo
import plotly.express as px
import json
import plotly
import ast  # For safely evaluating strings containing Python expressions

app = Flask(__name__)

@app.route('/')
def index():
    # MongoDB connection
    client = pymongo.MongoClient("mongodb://localhost:27017/twitter_data")
    db = client["twitter_data"]  # Adjust the database name
    collection = db["SentimentalAnalysis"]  # Adjust the collection name

    # Fetch data from MongoDB and convert to DataFrame
    data = list(collection.find({}, {"_id": 0, "value": 1}))
    df = pd.DataFrame([ast.literal_eval(d['value']) for d in data if 'value' in d])


    # Group by entity and sentiment, then count
    grouped_df = df.groupby(['entity', 'sentiment']).size().reset_index(name='count')

    # Create the Plotly bar chart with legend
    fig = px.bar(grouped_df, x='sentiment', y='count', color='entity', barmode='group')

    # Count sentiments
    # sentiment_counts = df['sentiment'].value_counts()

    # # Convert to DataFrame for Plotly
    # sentiment_df = sentiment_counts.reset_index()
    # sentiment_df.columns = ['sentiment', 'count']

    # # Create the Plotly bar chart
    # fig = px.bar(sentiment_df, x='sentiment', y='count')
    
    graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('index.html', graph_json=graph_json)

if __name__ == '__main__':
    app.run(debug=True)
