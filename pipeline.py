import pika
import json

def RabbitMQ(queueName, responseStr):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queueName)

    channel.basic_publish(exchange='', routing_key=queueName, body=responseStr)
    print(" [x] Sent" + responseStr)
    connection.close()