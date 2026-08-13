import numpy as np

def calculate_iou(box1,box2):
    """
        计算两个目标框IoU

        box格式:
        [x1,y1,x2,y2]
    """

    #计算交集区域
    x_left=max(box1[0],box2[0])
    y_top=max(box1[1],box2[1])

    x_right=min(box1[2],box2[2])
    y_bottom=min(box1[3],box2[3])

    #没有重叠
    if x_right<x_left or y_bottom<y_top:
        return 0

    #交集面积
    intersection=(x_right-x_left)*(y_bottom-y_top)

    #box1面积
    area1=((box1[2]-box1[0])*(box1[3]-box1[1]))

    #box2面积
    area2=((box2[2]-box2[0])*(box2[3]-box2[1]))


    union=area1+area2-intersection

    return intersection/union
