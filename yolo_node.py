import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2
from cv_bridge import CvBridge
from ultralytics import YOLO

class YoloNode(Node):           # 定義YoloNode具有ros2 node的所有功能
    def __init__(self):
        super().__init__('yolo_node')           # 初始化並命名為yolo_node
        
        self.subscription = self.create_subscription(                   
            Image, '/camera/image_raw', self.image_callback, 1)         # 建立subscriber，訂閱 '/camera/image_raw' 主題，資料類型 : Image，訊息進來呼叫self.image_callback處理，queue size : 1
        
        # (選修) 發布偵測結果話題
        self.result_pub = self.create_publisher(String, '/yolo_detections', 10)     # 建立subscriber，訂閱 '/yolo_detections'主題，資料類型 : String，10 : queue size
        
        self.model = YOLO('yolov8n.pt')             # 初始化 YOLOv8n 模型,第一次執行會自動下載 .pt 檔
        self.bridge = CvBridge()
        
        self.get_logger().info('YOLO Node (v8n) has been started.')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')     # 轉換 ROS 影像回 OpenCV 格式
        results = self.model.predict(source=frame, conf=0.4, imgsz=320, verbose=False)      # 推理，source=frame : 輸入影像，conf=0.4 : 信心度低於0.4會被忽略，imgsz=320 : 輸入影像縮小到320*320

        for result in results:
            boxes = result.boxes            # 取得偵測到的外型
            for box in boxes:
                cls_id = int(box.cls[0])        # 類別索引
                conf = float(box.conf[0])       # 信心度
                name = self.model.names[cls_id] # 透過索引查表得到名稱
                
                coords = box.xyxy[0].tolist() 
                x1, y1, x2, y2 = coords     # xmin,ymin,xmax,ymax
    
                # 在 Log 中印出位置 
                self.get_logger().info(f'Detected: {name} ({conf:.2f}) at [{int(x1)}, {int(y1)}, {int(x2)}, {int(y2)}]')
    
                res_msg = String()
                res_msg.data = f'{name}:{conf:.2f}:[{int(x1)},{int(y1)},{int(x2)},{int(y2)}]'
                self.result_pub.publish(res_msg)
            
            annotated_frame = result.plot()     # 繪製圖片
            #cv2.imwrite('latest_detection.jpg', annotated_frame)
            cv2.imshow("YOLOv8 Real-time Detection", annotated_frame)   # 顯示影像 
            cv2.waitKey(1)

def main(args=None):
    rclpy.init(args=args)           # 初始化ros2通訊環境
    node = YoloNode()               # 實例化
    try:
        rclpy.spin(node)            # 使程式保持執行
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        node.destroy_node()         # 摧毀node
        rclpy.shutdown()            # 關閉ros2通訊

if __name__ == '__main__':          # 確保這段程式只有在直接執行該檔案時才會運行
    main()