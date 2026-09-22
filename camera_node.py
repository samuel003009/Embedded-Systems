import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class CameraNode(Node):     # 定義CameraNode具有ros2 node的所有功能
    def __init__(self):
        super().__init__('camera_node')         # 初始化並命名為camera_node
        self.publisher_ = self.create_publisher(Image, '/camera/image_raw', 10)         # 建立一個publisher，Image : 傳輸主題，'/camera/image_raw' : topic，10 : queue size
        
        self.timer_period = 0.5             # 設定發布頻率為2Hz
        self.timer = self.create_timer(self.timer_period, self.timer_callback)      # 每0.1秒觸發一次timer_callback
        
        self.cap = cv2.VideoCapture(0, cv2.CAP_V4L2)      # 開啟編號為0的攝影機，使用 CAP_V4L2 後端
        self.cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))       # 強制設定影像格式為 MJPG，避免 USB 頻寬不足導致 timeout
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)         # 設定解析度 320*240
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)            # 只保留一張最新影像
        self.bridge = CvBridge()            # 初始化格式轉換器 
        self.get_logger().info('Camera Node has been started.')

    def timer_callback(self):
        ret, frame = self.cap.read()
        if ret:
            img_msg = self.bridge.cv2_to_imgmsg(frame, encoding="bgr8")     # 將 OpenCV 的 BGR 格式影像轉換為 ros2 影像訊息
            self.publisher_.publish(img_msg)                # 將這行資料送到ros2網路上
            cv2.imwrite('/home/ubuntu/ros2_ws/src/balloon_pop_bot/balloon_pop_bot/latest_camera_frame.jpg', frame)
        else:
            self.get_logger().warn('Failed to capture frame from camera.')

    def destroy_node(self):
        self.cap.release()          # 釋放攝影機占用資源
        super().destroy_node()      # 摧毀node

def main(args=None):
    rclpy.init(args=args)           # 初始化ros2通訊環境
    node = CameraNode()             # 實例化
    try:
        rclpy.spin(node)            # 使程式保持執行
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()         # 摧毀node
        rclpy.shutdown()            # 關閉ros2通訊

if __name__ == '__main__':
    main()
