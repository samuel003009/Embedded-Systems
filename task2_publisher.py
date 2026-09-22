import rclpy
from rclpy.node import Node
from std_msgs.msg import String
import Adafruit_DHT

class DH11Publisher(Node):      # 定義DH11Publisher具有ros2 node的所有功能
    def __init__(self):
        super().__init__('dh11_publisher')          # 初始化並命名為dh11_publisher
        self.publisher_ = self.create_publisher(String, 'DH11TH', 10)       # 建立一個publisher，String : 傳輸主題，'DH11TH' : topic，10 : queue size
        self.sensor = Adafruit_DHT.DHT11            # 設定感應器類型為DH11
        self.pin = 4                    # 連接的 GPIO 腳位
        self.timer = self.create_timer(2.0, self.timer_callback)            # 設定每2秒觸發一次，執行self.timer_callback
        self.get_logger().info('The publisher node has started, detecting DHT11...')

    def timer_callback(self):
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)      # 重複嘗試讀取數據
        if humidity is not None and temperature is not None:
            msg = String()
            msg.data = f'溫度:{temperature:.1f}C, 濕度:{humidity:.1f}%'
            self.publisher_.publish(msg)            # 將這行資料送到ros2網路上
            self.get_logger().info(f'Published data: "{msg.data}"')
        else:
            self.get_logger().warn('Unable to read data from the sensor')

def main(args=None):
    rclpy.init(args=args)       # 初始化ros2通訊環境
    node = DH11Publisher()      # 實例化
    try:
        rclpy.spin(node)        # 使程式保持執行
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()     # 摧毀node
        rclpy.shutdown()        # 關閉ros2通訊