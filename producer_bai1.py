"""Bai 1 - Producer: gui message chao mung vao queue iot_lab_queue."""
import sys
import time
import pika

HOST = "localhost"
QUEUE = "iot_lab_queue"
HO_TEN = "Lê Doãn Trung"     
MSSV = "B23DCCN854"            


def main():
    # So message can gui (mac dinh 1): python producer_bai1.py 5
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)

    for i in range(1, n + 1):
        body = f"Xin chao tu ung dung Python AMQP - {MSSV} - {HO_TEN}"
        if n > 1:
            body += f" (#{i})"
        channel.basic_publish(
            exchange="",                  # default exchange
            routing_key=QUEUE,            # default exchange route theo ten queue
            body=body.encode("utf-8"),
            properties=pika.BasicProperties(delivery_mode=2),  # persistent
        )
        print(f"Da gui: {body}")
        time.sleep(0.5)

    connection.close()


if __name__ == "__main__":
    main()
