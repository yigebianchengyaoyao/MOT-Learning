from ultralytics import YOLO

#加载模型

model=YOLO(
    "yolov8n.pt"
)


#视频目标追踪

results=model.track(
    #输入视频
    source="videos/test.mp4",
    #ByteTrack追踪器
    tracker="bytetrack.yaml",
    #使用GPU
    device=0,
    #保存结果
    save=True
)
print("追踪完成")