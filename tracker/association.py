import numpy as np
from scipy.optimize import linear_sum_assignment

from tracker.simple_tracker import calculate_iou

def associate_detections_to_tracks(
        detections,
        tracks,
        iou_threshold=0.3
):
    """
    使用IoU 和 Hungarian Algorithm
    对detections和tracks 进行匹配
    返回：
    matches
    unmatched——detections
    unmatched——tracks

    :param detections:
    :param tracks:
    :param iou_threshold:
    :return:
    """

    #没有轨迹时
    if len(tracks)==0:
        return(
            [],
            [],
            list(range(len(tracks)))
        )

    #创建IoU矩阵

    iou_matrix=np.zeros(
        (
            len(tracks),
            len(detections)
        ),
        dtype=np.float32
    )

    for track_index,track in enumerate(tracks):
        for detection_index,detection in enumerate(detections):
            iou_matrix[
                track_index,
                detection_index
            ]=calculate_iou(
                track.bbox,
                detection
            )

    cost_matrix=1-iou_matrix
    #匈牙利匹配
    track_indices,detection_indices=(
        linear_sum_assignment(
            cost_matrix
        )
    )
    matches=[]
    unmatched_tracks=list(
        range(len(tracks))
    )
    unmatched_detections = list(
        range(len(detections))
    )

    # -----------------------------
    # 4. 根据IoU阈值过滤
    # -----------------------------

    for track_index, detection_index in zip(
            track_indices,
            detection_indices
    ):

        iou = iou_matrix[
            track_index,
            detection_index
        ]

        # IoU太低，不接受这个匹配
        if iou < iou_threshold:
            continue

        matches.append(
            (
                track_index,
                detection_index
            )
        )

        unmatched_tracks.remove(
            track_index
        )

        unmatched_detections.remove(
            detection_index
        )

    return (
        matches,
        unmatched_detections,
        unmatched_tracks
    )