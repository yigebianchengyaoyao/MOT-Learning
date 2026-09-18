from ultralytics import YOLO
import cv2

from tracker.sort_tracker import SortTracker

model=YOLO("yolov8n.pt")

#使用自制的SORT追踪器
tracker=SortTracker(
    max_age=5,
    iou_threshold=0.3
)

video_path="videos/test.mp4"

cap=cv2.VideoCapture(video_path)

frame_index=0

while True:
    ret,frame=cap.read()

    if not ret:
        break

    frame_index+=1

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

        #未匹配到检测的轨迹用黄色标出，
        #这些框是Kalman预测出来的，不是YOLO检测到的
        if track.missed>0:
            color=(0,255,255)
        else:
            color=(0,255,0)

        cv2.rectangle(
            frame,
            (x1,y1),
            (x2,y2),
            color,
            2
        )

        cv2.putText(
            frame,
            f"ID:{track_id}",
            (x1,y1-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

    cv2.putText(
        frame,
        f"Frame:{frame_index}  Tracks:{len(tracks)}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,0,255),
        2
    )

    cv2.imshow("sort mot",frame)

    if cv2.waitKey(1)&0xff==27:
        break

cap.release()
cv2.destroyAllWindows()