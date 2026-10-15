"""Bai 2 - Sensor Producer: mo phong cam bien gui du lieu JSON moi 3 giay."""
import json
import random
import sys
import time
from datetime import datetime

import pika

HOST = "localhost"
QUEUE = "sensor_data_queue"
INTERVAL = 3  # giay


def main():
    # Mo rong: chay nhieu cam bien -> python sensor_producer_bai2.py sensor02
    device_id = sys.argv[1] if len(sys.argv) > 1 else "sensor01"

    connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE, durable=True)

    print(f"[{device_id}] bat dau gui du lieu moi {INTERVAL}s. Ctrl+C de dung.")
    try:
        while True:
            payload = {
                "device_id": device_id,
                "temperature": round(random.uniform(25.0, 40.0), 1),
                "humidity": round(random.uniform(30.0, 80.0), 1),
                "timestamp": datetime.now().isoformat(timespec="seconds"),
            }
            channel.basic_publish(
                exchange="",
                routing_key=QUEUE,
                body=json.dumps(payload),
                properties=pika.BasicProperties(
                    content_type="application/json", delivery_mode=2
                ),
            )
            print("Da gui:", payload)
            time.sleep(INTERVAL)
    except KeyboardInterrupt:
        print("\nDa dung sensor.")
    finally:
        connection.close()


if __name__ == "__main__":
    main()
