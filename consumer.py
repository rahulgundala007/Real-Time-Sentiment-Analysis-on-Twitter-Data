from confluent_kafka import Consumer, KafkaError, KafkaException

def create_consumer(config):
    return Consumer(config)

def consume_messages(consumer, topics):
    try:
        consumer.subscribe(topics)

        while True:
            msg = consumer.poll(1.0)  # Poll for messages with a 1-second timeout
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    # End of partition event
                    print(f"Reached end of partition {msg.partition()} at offset {msg.offset()}")
                else:
                    raise KafkaException(msg.error())
            else:
                print(f"Received message: {msg.value().decode('utf-8')}")
    except KeyboardInterrupt:
        print("Consumer interrupted by user.")
    finally:
        consumer.close()

# Kafka configuration
config = {
    'bootstrap.servers': 'localhost:9092',  # Change as per your server configuration
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}

if __name__ == "__main__":
    # Creating a Kafka consumer instance
    consumer = create_consumer(config)

    # Consuming messages from the 'twitter_data' topic
    consume_messages(consumer, ['twitter_data'])
