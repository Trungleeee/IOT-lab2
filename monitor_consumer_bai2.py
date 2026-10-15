"""Bai 2 - Monitoring Consumer: nhan JSON, in du lieu va canh bao nguong."""
import json
import pika

HOST = "localhost"
QUEUE = "sensor_data_queue"
TEMP_MAX = 35
HUMI_MIN = 40


def on_message(ch, method, properties, body):
    try:
        data = json.loads(body)
        device = data["device_id"]
        temp = float(data["temperature"])
        humi = float(data["humidity"])
    except (ValueError, KeyError, TypeError) as e:
        print(f"Payload khong hop le ({e}): {body!r}")
        ch.basic_ack(delivery_tag=method.delivery_tag)  # bo message loi
        return

    print(f"Device: {device}")
    print(f"Temperature: {temp}")
    print(f"Humidity: {humi}")
    if "timestamp" in data:
        print(f"Time: {data['timestamp']}")
    if temp > TEMP_MAX:
        print("CANH BAO: Nhiet do cao")
    if humi < HUMI_MIN:
        print("CANH BAO: Do am thap")
    print("-" * 40)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)
    channel.basic_consume(queue=QUEUE, on_message_callback=on_message)
    print(f"Dang giam sat '{QUEUE}'. Ctrl+C de dung.")
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        print("\nDa dung monitor.")
        channel.stop_consuming()
    finally:
        connection.close()


if __name__ == "__main__":
    main()
