"""Bai 1 - Consumer: nhan message tu iot_lab_queue, in noi dung + thoi diem nhan."""
from datetime import datetime
import pika

HOST = "localhost"
QUEUE = "iot_lab_queue"


def on_message(ch, method, properties, body):
    print(f"Da nhan message: {body.decode('utf-8')}")
    print(f"Thoi gian nhan: {datetime.now().strftime('%H:%M:%S')}")
    print("-" * 40)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)

    print(f"Dang cho message tren '{QUEUE}'. Nhan Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung consumer.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
