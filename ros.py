import rclpy
from rclpy.node import Node
import serial
from std_msgs.msg import Float32  # 匯入 Float32 訊息格式以滿足發布要求

class TempBridgeNode(Node):
    def __init__(self):
        super().__init__('temp_bridge_node')        # 節點在ros網路中叫做temp_bridge_node
        
        # 開啟序列埠連線
        try:
            self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)       # 讀不到資料1秒跳過
            self.get_logger().info('Serial port /dev/ttyACM0 opened successfully.')
        except Exception as e:
            self.get_logger().error(f'Failed to open serial port: {str(e)}')
            return

        # 清除初始快取資料，確保讀到最新值
        self.ser.reset_input_buffer()
        
        # 建立publisher，主題名稱為 "/temperature"，資料類型為 Float32，10 : queue size
        self.publisher_ = self.create_publisher(Float32, '/temperature', 10)
        
        # 建立timer，每 2 秒執行一次讀取動作
        self.timer = self.create_timer(2.0, self.read_serial_data)
        
        self.get_logger().info('UART Temp Reader Node with Publisher has started.')

    def read_serial_data(self):
        # 檢查序列埠是否有資料進來
        if self.ser.in_waiting > 0:
            try:
                # 讀取一行、解碼成UTF-8文字並去掉空白
                raw_data = self.ser.readline().decode('utf-8', errors='ignore').strip()
                
                if raw_data:
                    # 顯示原始資料內容
                    # self.get_logger().info(f'Raw Data: {raw_data}')
                    
                    # 解析資料：從 "Temp: 25.00°C" 中提取數值
                    if "Temp" in raw_data:
                        try:
                            # 擷取冒號之後、°C 之前的文字並轉為浮點數
                            temp_str = raw_data.split(':')[1].split('°C')[0].strip()
                            temp_float = float(temp_str)
                            
                            # 使用 ROS 2 Logging 紀錄數值
                            self.get_logger().info(f'Parsed Temperature: {temp_float}°C')
                            
                            # 發布到 Topic
                            msg = Float32()
                            msg.data = temp_float
                            self.publisher_.publish(msg)        # 把訊息丟到/temperature這個Topic 上
                            
                        except (IndexError, ValueError) as parse_error:
                            self.get_logger().warn(f'Parse error: {parse_error}')
                        
            except Exception as e:
                self.get_logger().error(f'Error reading serial: {str(e)}')

def main(args=None):                # 初始化ros2環境
    rclpy.init(args=args)
    node = TempBridgeNode()         # 實例化
    try:
        rclpy.spin(node)            # 無限循環
    except KeyboardInterrupt:
        node.get_logger().info('Node stopped by user.')
    finally:
        # 確保關閉序列埠並釋放資源
        if hasattr(node, 'ser'):
            node.ser.close()
        node.destroy_node()     # 摧毀節點釋放記憶體
        rclpy.shutdown()        # 關閉ros2

if __name__ == '__main__':      # 如果檔案直接執行，執行main()
    main()
