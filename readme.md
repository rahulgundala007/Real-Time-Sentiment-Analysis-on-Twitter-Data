# Sentiment-Analysis
Real-Time Sentiment Analysis on Twitter Data
Project Overview

This project focuses on building a real-time sentiment analysis system for Twitter data. The rise of social media has amplified the need for brands to monitor customer sentiment. This system aims to classify tweets into positive, negative, or neutral sentiments and detect mentions of company competitors, enabling businesses to manage their online reputation proactively.

Key Features

•	Near real-time analysis of customer sentiment from Twitter data.
•	Classification of each tweet into positive, negative, or neutral categories.
•	Optional detection of mentions of company competitors.
•	Aggregation of results for dashboard visualization and Datawarehouse storage for OLAP.

Architecture

The solution architecture adheres to the guidelines provided, with justifiable deviations documented in the project report.

Implementation Steps
Environment Setup:

•	Install Python 3.9, Java JRE, Zookeeper for Kafka, Apache Kafka, Spark with Hadoop, and Spark Streaming.
•	Choose and deploy a NoSQL store and an optional Datawarehouse for batch and analytical processing, respectively.
•	Twitter API Integration: (But we have used a csv file)
•	Data Pipeline with Kafka: Set up Kafka brokers, partitions, and topics.
•	Implement Kafka Consumer and Producer in Python.
•	Spark-Kafka Integration: Create a Spark session to read the Twitter stream. Apply data transformations and sentiment analysis on each tweet using libraries like TextBlob.
•	We have written results back to a Kafka topic for dashboard consumption.
Data Persistence:

•	We have selected MongoDB to Integrate the NoSQL store with Kafka to write tweets into it.
•	Dashboard Web Application: we Developed a web application using Flask to serve as a real-time dashboard for sentiment analysis and competition detection.

