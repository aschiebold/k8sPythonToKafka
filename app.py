from confluent_kafka import Producer, Consumer, KafkaException
import sys
import threading

# Kafka configuration
bootstrap_servers = 'kafka-service:9092'
topic = 'test-topic'

# Producer configuration
producer_conf = {
    'bootstrap.servers': bootstrap_servers
}

# Consumer configuration
consumer_conf = {
    'bootstrap.servers': bootstrap_servers,
    'group.id': 'python-consumer',
    'auto.offset.reset': 'earliest'
}

# Initialize producer and consumer
producer = Producer(producer_conf)
consumer = Consumer(consumer_conf)
consumer.subscribe([topic])

# Producer callback
def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

# Consumer function (runs in a separate thread)
def consume_messages():
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            print(f'Received message: {msg.value().decode("utf-8")}')
    except KeyboardInterrupt:
        pass
    finally:
        consumer.close()

# Start consumer in a separate thread
consumer_thread = threading.Thread(target=consume_messages)
consumer_thread.daemon = True
consumer_thread.start()

# Main loop for producing messages
try:
    while True:
        # Get input from user
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break
        # Produce message to Kafka
        producer.produce(topic, message.encode('utf-8'), callback=delivery_report)
        producer.flush()
except KeyboardInterrupt:
    pass
finally:
    print("Shutting down...")