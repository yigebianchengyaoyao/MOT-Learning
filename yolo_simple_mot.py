from ultralytics import YOLO
import cv2

from tracker.tracker import SimpleTracker

model=YOLO("yolov8n.pt")

tracker=SimpleTracker()

video_path="videos/test.mp4"

cap=cv2.VideoCapture(video_path)

while True:
    ret,frame=cap.read()

    if not ret:
        break

    #yolo检测
    results=model(frame,device=0,verbose=False)

    detections=[]

    #提取bbox
    for result in results:
        boxes=result.boxes
        for box in boxes:
            #类别
            cls=int(box.cls[0])

            #只追踪人
            if cls !=0:
                continue

            #坐标
            x1,y1,x2,y2=(
                box.xyxy[0].cpu().numpy()
            )

            detections.append(
                [
                    x1,y1,x2,y2
                ]
            )

    #tracker更新

    tracks=tracker.update(detections)

    #绘制ID
    for track in tracks:
        x1,y1,x2,y2=map(int,track.bbox)
        track_id=track.id

        cv2.rectangle(
            frame,
            (x1,y1),
            (x2,y2),
            (0,255,0),
            2
        )

        cv2.putText(
            frame,
            f"ID:{track_id}",
            (x1,y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0,255,0),
            2
        )

    cv2.imshow("simple mot",frame)

    if cv2.waitKey(1)&0xff==27:
        break

cap.release()
cv2.destroyAllWindows()