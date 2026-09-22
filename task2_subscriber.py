import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class DH11Subscriber(Node):         # 定義DH11Subscriber具有ros2 node的所有功能
    def __init__(self):
        super().__init__('dh11_subscriber')          # 初始化並命名為dh11_subscriber
        
        self.subscription = self.create_subscription(       # 建立subscriber，訂閱 "DH11TH" 主題，資料類型 : String，訊息進來呼叫self.listener_callback處理，queue size : 10
            String,
            'DH11TH',
            self.listener_callback,
            10)
        self.get_logger().info('The subscriber node has started and is waiting to receive data....')

    def listener_callback(self, msg):           # 訊息送進來時，呼叫這個函式
        self.get_logger().info(f'[Received successfully] Value is: {msg.data}')

def main(args=None):
    rclpy.init(args=args)           # 初始化ros2通訊環境
    node = DH11Subscriber()
    try:
        rclpy.spin(node)            # 使程式保持執行
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()         # 摧毀node
        rclpy.shutdown()            # 關閉ros2通訊