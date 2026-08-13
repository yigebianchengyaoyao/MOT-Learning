from ultralytics import YOLO

model=YOLO("yolov8n.pt")

results=model(
    "./picture/行人.png",
    device=0
)

for result in results:
    #检测框
    boxes=result.boxes
    print(result.names)

    for box in boxes:
        #坐标
        xyxy=box.xyxy
        #置信度
        conf=box.conf
        #类别
        cls=box.cls

        print(
            "位置：",
            xyxy
        )

        print(
            "置信度：",
            conf
        )

        print(
            "类别：",
            cls
        )
