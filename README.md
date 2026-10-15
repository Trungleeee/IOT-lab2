# Thực hành Python với giao thức AMQP

## Broker sử dụng
RabbitMQ chạy local (`localhost`, cổng AMQP mặc định **5672**), user `guest/guest`, thư viện Python `pika`.
Nếu dùng broker chung của lớp, sửa biến `HOST` ở đầu mỗi file.

## Cài đặt
```
pip install pika
```
Trước khi chạy, sửa `HO_TEN` và `MSSV` trong `producer_bai1.py`.

## Cách chạy (mỗi lệnh một terminal)
**Bài 1** – producer → queue `iot_lab_queue` → consumer
```
python consumer_bai1.py
python producer_bai1.py        # thêm số để gửi nhiều message: python producer_bai1.py 5
```
**Bài 2** – cảm biến gửi JSON mỗi 3 giây vào `sensor_data_queue`
```
python monitor_consumer_bai2.py
python sensor_producer_bai2.py            # sensor01
python sensor_producer_bai2.py sensor02   # mở rộng: nhiều cảm biến
```
**Bài 3** – direct exchange `iot_alert_exchange`
```
python warning_consumer_bai3.py    # queue warning_queue, key "warning"
python critical_consumer_bai3.py   # queue critical_queue, key "critical"
python alert_producer_bai3.py      # gửi info, warning, critical
```
Chạy consumer trước producer để queue đã được bind khi message được gửi.

## Kết quả đạt được
- Bài 1: gửi/nhận message qua queue, in nội dung và giờ nhận; consumer chạy liên tục đến khi Ctrl+C; producer gửi được nhiều message.
- Bài 2: payload JSON (có thêm `timestamp`) gửi tuần hoàn 3 giây; consumer in device/temperature/humidity và cảnh báo khi nhiệt độ > 35 hoặc độ ẩm < 40; chạy được nhiều sensor.
- Bài 3: direct exchange phân phối đúng: `info` không queue nào nhận, `warning` chỉ vào `warning_queue`, `critical` chỉ vào `critical_queue`.
