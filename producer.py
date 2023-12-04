from confluent_kafka import Producer
import json
import csv
import time

def delivery_report(err, msg):
    if err is not None:
        print(f"Message delivery failed: {err}")
    else:
        print(f"Message delivered to {msg.topic()} [{msg.partition()}]")

def create_producer(config):
    return Producer(config)

def send_message(producer, topic, key, value):
    producer.produce(
        topic=topic, 
        key=str(key), 
        value=json.dumps(value), 
        callback=delivery_report
    )
    producer.poll(0)

def close_producer(producer):
    producer.flush()

def send_csv_data(producer, topic, csv_file, rows_per_second):
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for i, row in enumerate(reader):
            send_message(producer, topic, row['tweet_id'], row)
            # Send a specific number of rows per second
            if i % rows_per_second == rows_per_second - 1:
                time.sleep(1)

# Kafka configuration
config = {
    'bootstrap.servers': 'localhost:9092',  # Change as per your server configuration
}

# CSV file path
csv_file_path = r"C:\Users\bhanu\Downloads\twitter_training.csv"

# Creating a Kafka producer instance
producer = create_producer(config)

# Define how many rows per second you want to send
rows_per_second = 5  # Adjust this number as needed

# Sending data from CSV file to Kafka topic
send_csv_data(producer, 'twitter_data', csv_file_path, rows_per_second)  # Replace 'rawdata' with your topic name

# Close the producer
close_producer(producer)