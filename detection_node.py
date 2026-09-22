import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO
import serial
import time
import torch

torch.set_num_threads(2)

class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')
        self.subscription = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 1)
        
        # 發布包含畫好框的影像
        self.image_pub = self.create_publisher(Image, '/camera/image_annotated', 1)

        self.model = YOLO('/home/ubuntu/ros2_ws/best.onnx')             
        self.bridge = CvBridge()
        self.is_processing = False


        # 序列埠連線
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1, write_timeout=0)
            time.sleep(2) 
            self.get_logger().info('Serial connection established with Arduino.')
        except Exception as e:
            self.get_logger().error(f'Failed to connect to Arduino: {e}')
            self.ser = None

        self.last_seen_time = time.time()
        self.get_logger().info('Detection Node started.')

    def image_callback(self, msg):
        if self.is_processing:
            return 
        self.is_processing = True

        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        # 推論目標 
        results = self.model.predict(source=frame, conf=0.6, imgsz=320, verbose=False)

        # 畫出所有氣球的框線與機率
        annotated_frame = results[0].plot()

        largest_area = 0
        target_cx = -1
        target_cy = -1 
        current_time = time.time()
        command = 'S' 

        # 找畫面中最大的氣球
        for result in results:
            for box in result.boxes:
                coords = box.xyxy[0].tolist() 
                x1, y1, x2, y2 = coords
                cx = int((x1 + x2) / 2)
                cy = int((y1 + y2) / 2)
                area = int((x2 - x1) * (y2 - y1))

                if area > largest_area:
                    largest_area = area
                    target_cx = cx
                    target_cy = cy

        # 在被鎖定的最大氣球中心點，補上一個實心紅點和文字
        if largest_area > 0:
            cv2.imwrite('/home/ubuntu/ros2_ws/src/balloon_pop_bot/balloon_pop_bot/latest_detected_balloon.jpg', annotated_frame)
            self.get_logger().info('Saved latest_detected_balloon.jpg to SD Card')

        # 將畫完的畫面轉回 ROS 格式並發布出去
        annotated_msg = self.bridge.cv2_to_imgmsg(annotated_frame, encoding="bgr8")
        self.image_pub.publish(annotated_msg)

        # 馬達控制邏輯
        if largest_area > 0:
            self.last_seen_time = current_time
            CLOSE_AREA_THRESHOLD = 25000 

            if target_cx < 120:
                command = 'L' 
                self.get_logger().info(f'Tracking: L (cx:{target_cx})')
            elif target_cx > 200:
                command = 'R' 
                self.get_logger().info(f'Tracking: R (cx:{target_cx})')
            else:
                if largest_area >= CLOSE_AREA_THRESHOLD:
                    command = 'A' 
                    self.get_logger().info(f'Tracking: A (SUPER CLOSE!)')
                else:
                    command = 'F' 
                    self.get_logger().info(f'Tracking: F (Target locked)')
        else:
            if current_time - self.last_seen_time > 5.0:
                command = 'R' 
                self.get_logger().info('Lost balloon for 5s! Searching -> R')
            else:
                command = 'S'
                self.get_logger().info('No balloons detected -> S')

        # 傳輸指令給 Arduino
        if self.ser is not None:
            try:
                self.ser.write(command.encode('utf-8'))
                self.ser.flush()
            except Exception as e:
                pass

        self.is_processing = False

def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node.ser is not None:
            node.ser.write(b'S') 
            node.ser.close()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
