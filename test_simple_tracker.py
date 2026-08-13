from tracker.tracker import  SimpleTracker

tracker=SimpleTracker()

#第一帧

frame1 = [

    [100,100,200,300],

    [400,100,500,300]

]

tracks=tracker.update(frame1)
print("第一帧")

for t in tracks:
    print(
        "ID:",
        t.id,
        "bbox:",
        t.bbox
    )

#第二帧
frame2 = [

    [110,105,210,305],

    [410,105,510,305]

]

tracks=tracker.update(frame2)
print("\n第二帧")

for t in tracks:
    print(
        "ID:",
        t.id,
        "bbox:",
        t.bbox
    )
