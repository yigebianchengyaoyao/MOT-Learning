from tracker.simple_tracker import calculate_iou

box1=[
    100,
    100,
    200,
    300
]

box2=[
    120,
    120,
    220,
    320
]

iou=calculate_iou(
    box1,box2
)

print("IoU:",iou)
