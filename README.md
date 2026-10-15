# Thực hành Python với giao thức AMQP

- Sinh viên: Lê Doãn Trung
- Mã sinh viên: B23DCCN854

## 1. Môi trường và broker

| Mục | Giá trị |
|---|---|
| Broker | RabbitMQ 4.3.6, cài trên Windows, chạy dưới dạng dịch vụ |
| Địa chỉ | `localhost`, cổng AMQP mặc định `5672` |
| Tài khoản | `guest` / `guest` |
| Giao diện quản lý | http://localhost:15672 (đã bật plugin `rabbitmq_management`) |
| Ngôn ngữ | Python 3.14, thư viện `pika` |

Cài thư viện:
```
pip install pika
```

Kiểm tra broker đang chạy (PowerShell), kết quả phải là `TcpTestSucceeded : True`:
```
Test-NetConnection localhost -Port 5672
```
Nếu `False`: mở `services.msc`, tìm dịch vụ **RabbitMQ** và chọn Start.

Nếu dùng broker khác (broker chung của lớp), sửa biến `HOST` ở đầu mỗi file `.py`.

## 2. Danh sách file

| File | Bài | Vai trò |
|---|---|---|
| `producer_bai1.py` | 1 | Gửi message chào mừng vào `iot_lab_queue` |
| `consumer_bai1.py` | 1 | Nhận message, in nội dung và giờ nhận |
| `sensor_producer_bai2.py` | 2 | Mô phỏng cảm biến, gửi JSON mỗi 3 giây vào `sensor_data_queue` |
| `monitor_consumer_bai2.py` | 2 | Nhận JSON, in số liệu và cảnh báo |
| `alert_producer_bai3.py` | 3 | Gửi cảnh báo info/warning/critical lên exchange |
| `warning_consumer_bai3.py` | 3 | Queue `warning_queue`, routing key `warning` |
| `critical_consumer_bai3.py` | 3 | Queue `critical_queue`, routing key `critical` |

## 3. Cách chạy

Mỗi lệnh chạy trong một terminal riêng. Trước tiên vào thư mục bài:
```
cd C:\Users\Lenovo\Downloads\amqp_lab
```
Nguyên tắc chung: **chạy consumer trước, producer sau**. Dừng chương trình bằng `Ctrl+C`.

### Bài 1: producer → queue → consumer

Terminal 1:
```
python consumer_bai1.py
```
Terminal 2:
```
python producer_bai1.py          # gửi 1 message
python producer_bai1.py 5        # gửi 5 message liên tiếp
```
Kết quả ở consumer:
```
Da nhan message: Xin chao tu ung dung Python AMQP - B23DCCN854 - Lê Doãn Trung
Thoi gian nhan: 16:58:31
```

### Bài 2: cảm biến IoT gửi telemetry

Terminal 1:
```
python monitor_consumer_bai2.py
```
Terminal 2:
```
python sensor_producer_bai2.py
```
Mở rộng, thêm cảm biến (mỗi cái một terminal):
```
python sensor_producer_bai2.py sensor02
python sensor_producer_bai2.py sensor03
```
Dữ liệu nhiệt độ (25 đến 40 °C) và độ ẩm (30 đến 80 %) được **sinh ngẫu nhiên** bằng `random.uniform`, không đọc từ cảm biến thật.

Kết quả ở consumer:
```
Device: sensor01
Temperature: 38.3
Humidity: 49.1
Time: 2026-10-15T17:05:12
CANH BAO: Nhiet do cao
```
Cảnh báo: nhiệt độ > 35 in `CANH BAO: Nhiet do cao`; độ ẩm < 40 in `CANH BAO: Do am thap`.

### Bài 3: direct exchange và routing key

Terminal 1:
```
python warning_consumer_bai3.py
```
Terminal 2:
```
python critical_consumer_bai3.py
```
Terminal 3 (chạy sau cùng):
```
python alert_producer_bai3.py
```
Kết quả:
- Terminal 1: `[warning_queue] Da nhan: Nhiet do phong may chu vuot nguong warning`
- Terminal 2: `[critical_queue] Da nhan: Cam bien kho lanh mat ket noi critical`
- Message `info` không queue nào nhận (không có queue bind với key `info`).

Phải chạy hai consumer trước vì consumer là nơi tạo queue và bind vào exchange; nếu producer chạy trước thì message bị bỏ.

## 4. Kết quả đạt được

- **Bài 1:** kết nối được broker, gửi một hoặc nhiều message vào `iot_lab_queue`, consumer nhận đúng và hiển thị thời điểm nhận, chạy liên tục đến khi Ctrl+C.
- **Bài 2:** payload đúng định dạng JSON (có thêm trường `timestamp`), gửi tuần hoàn mỗi 3 giây, consumer phân tích đúng và phát hiện cảnh báo nhiệt độ/độ ẩm; chạy được nhiều cảm biến cùng lúc.
- **Bài 3:** tạo được direct exchange `iot_alert_exchange`, bind `warning_queue` và `critical_queue` đúng routing key, message được phân phối đúng nơi nhận.

## 5. Xử lý lỗi thường gặp

| Lỗi | Nguyên nhân và cách xử lý |
|---|---|
| Treo hoặc báo `AMQPConnectionError` khi kết nối | Broker chưa chạy. Khởi động dịch vụ RabbitMQ rồi chạy lại. |
| `KeyboardInterrupt` khi vừa chạy | Có Ctrl+C trong lúc nạp thư viện; chạy lại. |
| Bài 3 không có consumer nào nhận | Chạy producer trước consumer. Chạy lại theo đúng thứ tự. |
| Không mở được http://localhost:15672 | Chưa bật plugin hoặc chưa restart dịch vụ: `rabbitmq-plugins enable rabbitmq_management`, sau đó `net stop RabbitMQ` và `net start RabbitMQ` (cần quyền Administrator). |