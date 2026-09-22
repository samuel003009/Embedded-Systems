import cv2
import mediapipe as mp
import time

##### model : mediapipe



CONFIDENCE_THRESHOLD = 0.5  # 信心度門檻

# 初始化 MediaPipe 繪圖工具
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# 初始化手部與臉部模型
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=CONFIDENCE_THRESHOLD,
    min_tracking_confidence=CONFIDENCE_THRESHOLD
)

mp_face_mesh = mp.solutions.face_mesh
face_mesh_detector = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,          # 啟用refine_landmarks精準取得瞳孔與眼睛位置
    min_detection_confidence=CONFIDENCE_THRESHOLD,
    min_tracking_confidence=CONFIDENCE_THRESHOLD
)

print("已載入偵測模型...")

# 開啟相機，格式 : MJPG，640*480
cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)   
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

if not cap.isOpened():
    print("無法開啟相機...")
    exit()

frame_count = 0
last_fps_time = time.time()

try:
    while True:
        ret, frame = cap.read()     # ret : 有沒有抓到畫面，frame : 照片的數據
        if not ret:
            continue

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        imH, imW, _ = frame.shape           # 取得照片的高跟寬，_代表通道數忽略
        
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)      # 將BGR格式轉為AI模型
        annotated_frame = frame.copy()
        
        detected_hand = False
        detected_face = False

        # 偵測手部
        hand_results = hands_detector.process(image_rgb)
        if hand_results.multi_hand_landmarks:
            detected_hand = True
            for hand_landmarks in hand_results.multi_hand_landmarks:            # 繪製手部骨架
                
                mp_drawing.draw_landmarks(
                    annotated_frame, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
                
                # 標註手
                wrist = hand_landmarks.landmark[0]          # 0 : 手腕的位置
                cx, cy = int(wrist.x * imW), int(wrist.y * imH)         # wrist.x : 手腕的寬度比例，cx : 實際像素位置
                cv2.putText(annotated_frame, "Hand", (cx, cy - 10),         # (cx, cy-10) : 文字座標
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 偵測臉部
        face_results = face_mesh_detector.process(image_rgb)
        if face_results.multi_face_landmarks:
            detected_face = True
            for face_landmarks in face_results.multi_face_landmarks:
                
                mp_drawing.draw_landmarks(                                  # 繪製臉的輪廓線
                    image=annotated_frame, landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())

                # 標註左眼 
                le_pt = face_landmarks.landmark[33]
                cv2.putText(annotated_frame, "Eye", (int(le_pt.x * imW), int(le_pt.y * imH) - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                
                # 標註右眼 
                re_pt = face_landmarks.landmark[263]
                cv2.putText(annotated_frame, "Eye", (int(re_pt.x * imW), int(re_pt.y * imH) - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 0, 0), 1)
                
                # 標註鼻子 
                nose_pt = face_landmarks.landmark[4]
                cv2.putText(annotated_frame, "Nose", (int(nose_pt.x * imW), int(nose_pt.y * imH) - 5), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 0, 255), 1)

                # 標註嘴巴 
                mouth_pt = face_landmarks.landmark[0]
                cv2.putText(annotated_frame, "Mouth", (int(mouth_pt.x * imW), int(mouth_pt.y * imH) + 15), 
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 255), 1)

        # 檢查是否需要存檔
        if detected_hand or detected_face:
            print(f"發現目標...")
            filename = f"detected_labeled_{timestamp}.jpg"
            cv2.imwrite(filename, annotated_frame)
            print(f"已將照片儲存為: {filename}")
        
        time.sleep(0.01)

except KeyboardInterrupt:
    print("\n手動終止程式。")

finally:
    cap.release()
    print("結束，相機資源已釋放")