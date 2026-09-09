from tracker.kalman_tracker import KalmanTracker

bbox=[
    100,
    100,
    200,
    300
]

tracker=KalmanTracker(bbox)

#模拟目标向右移动

detections=[
    [110, 100, 210, 300],

    [120, 100, 220, 300],

    [130, 100, 230, 300],

    [140, 100, 240, 300]
]
for i,det in enumerate(detections):
    #先预测
    predicted=tracker.predict()
    print(f"Frame {i+1}")
    print("预测位置：",predicted)
    print("检测位置",det)
    tracker.update(det)

    print("------------------")