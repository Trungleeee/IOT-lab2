"""Bai 3 - Alert Producer: gui canh bao len direct exchange iot_alert_exchange."""
import time
import pika

HOST = "localhost"
EXCHANGE = "iot_alert_exchange"

ALERTS = [
    ("info", "He thong IoT hoat dong binh thuong info"),
    ("warning", "Nhiet do phong may chu vuot nguong warning"),
    ("critical", "Cam bien kho lanh mat ket noi critical"),
]


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.exchange_declare(exchange=EXCHANGE, exchange_type="direct", durable=True)

    for routing_key, message in ALERTS:
        channel.basic_publish(
            exchange=EXCHANGE,
            routing_key=routing_key,
            body=message.encode("utf-8"),
        )
        print(f"Da gui [{routing_key}]: {message}")
        time.sleep(0.5)

    connection.close()


if __name__ == "__main__":
    main()
