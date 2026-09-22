import rclpy
from rclpy.node import Node
import Adafruit_DHT 

class Task1Node(Node):              # 定義Task1Node具有ros2 node的所有功能
    def __init__(self):
        super().__init__('task1_node')          # 初始化並命名為task1_node
        self.sensor = Adafruit_DHT.DHT11        # 設定感應器類型為DH11  
        self.pin = 4    # 連接的 GPIO 腳位
        self.timer = self.create_timer(2.0, self.timer_callback)        # 設定每2秒觸發一次，執行self.timer_callback
        self.get_logger().info('Detect DHT11...')

    def timer_callback(self):           # 每隔2秒執行一次
        humidity, temperature = Adafruit_DHT.read_retry(self.sensor, self.pin)          # 重複嘗試讀取數據
        if humidity is not None and temperature is not None:
            self.get_logger().info(f'溫度: {temperature:.1f}°C, 濕度: {humidity:.1f}%')
        else:
            self.get_logger().warn('Read failed')

def main(args=None):
    rclpy.init(args=args)       # 初始化ros2通訊環境
    node = Task1Node()          # 實例化
    rclpy.spin(node)            # 使程式保持執行
    rclpy.shutdown()            # 關閉ros2資源