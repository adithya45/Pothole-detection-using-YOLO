import cv2
import matplotlib.pyplot as plt
from ultralytics import YOLO

model = YOLO('best.pt')

image_path = r'C:\Users\user\Desktop\Pothole\datasets\Object-Detection-(Bounding-Box)-1\test\images\197_jpg.rf.e13be23f78121b88f6d78cef2ca475b3.jpg' 
image = cv2.imread(image_path)

results = model(image)

for result in results:
    boxes = result.boxes  
    for box in boxes:
        x1, y1, x2, y2 = box.xyxy[0]  
        conf = box.conf[0]             
        cls = box.cls[0]               

        if int(cls) == 0:  
            cv2.rectangle(image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)  
            
            label = f'pothole: {conf:.2f}'  
            
            font_scale = 0.5
            font_thickness = 2
            
            (w, h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, font_scale, font_thickness)
            
            cv2.rectangle(image, (int(x1), int(y1) - h - 10), (int(x1) + w, int(y1)), (0, 255, 0), -1)
            cv2.putText(image, label, (int(x1), int(y1) - 5), cv2.FONT_HERSHEY_SIMPLEX, font_scale, (255, 255, 255), font_thickness)

image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

plt.imshow(image_rgb)
plt.axis('off')  
plt.show()
