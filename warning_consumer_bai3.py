"""Bai 3 - Warning Consumer: chi nhan canh bao muc warning."""
import pika

HOST = "localhost"
EXCHANGE = "iot_alert_exchange"
QUEUE = "warning_queue"
ROUTING_KEY = "warning"


def on_message(ch, method, properties, body):
    print(f"[{QUEUE}] Da nhan: {body.decode('utf-8')}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct", durable=True)
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.queue_bind(queue=QUEUE, exchange=EXCHANGE, routing_key=ROUTING_KEY)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)

    print(f"[{QUEUE}] cho canh bao '{ROUTING_KEY}'. Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
