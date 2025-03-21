import cv2
from ultralytics import YOLO

model = YOLO('best.pt')

video_path = r'C:\Users\user\Desktop\Pothole\testing\video.mp4'
cap = cv2.VideoCapture(video_path)

frame_skip = 2  

while True:
    for _ in range(frame_skip):  
        ret = cap.grab() 
    ret, frame = cap.read()
    
    if not ret:
        break 

    results = model(frame)

    for result in results:
        boxes = result.boxes  
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  
            conf = box.conf[0]            
            cls = box.cls[0]              

            if int(cls) == 0:  
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                
                label = f'pothole: {conf:.2f}' 
                
               
                font_scale = 1.0
                font_thickness = 2
                
                (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
                
                cv2.rectangle(frame, (int(x1), int(y1) - h - 10), (int(x1) + w, int(y1)), (0, 255, 0), -1)
                cv2.putText(frame, label, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

    cv2.imshow('Video Detection', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
