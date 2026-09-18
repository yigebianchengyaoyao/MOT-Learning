from tracker.association import (
    associate_detections_to_tracks
)
from tracker.track import Track


class SortTracker:
    """
    完整SORT追踪器。

    与SimpleTracker的区别：
    1. 使用Kalman预测位置，而不是直接用上一帧检测框
    2. 使用匈牙利算法做全局最优匹配，而不是贪心匹配
    3. 有完整的轨迹生命周期管理（missed / max_age）
    """

    def __init__(
            self,
            max_age=5,
            iou_threshold=0.3
    ):
        #所有轨迹
        self.tracks=[]

        #下一个可用ID
        self.next_id=1

        #最多容忍连续丢失多少帧，超过就删除轨迹
        self.max_age=max_age

        #匹配阈值
        self.iou_threshold=iou_threshold

    def update(self,detections):
        """
        输入当前帧的检测框列表：
        [
            [x1,y1,x2,y2],
            ...
        ]

        返回当前所有存活轨迹。
        """

        # ---------------------------------
        # ① 每条轨迹先用Kalman预测下一帧位置
        # ---------------------------------
        for track in self.tracks:
            track.predict()

        # ---------------------------------
        # ② 用预测框与检测框计算IoU矩阵
        # ③ 匈牙利算法完成匹配
        # ---------------------------------
        (
            matches,
            unmatched_detections,
            unmatched_tracks
        )=associate_detections_to_tracks(
            detections,
            self.tracks,
            self.iou_threshold
        )

        # ---------------------------------
        # ④ 匹配成功：Kalman update
        # ---------------------------------
        for track_index,detection_index in matches:
            self.tracks[track_index].update(
                detections[detection_index]
            )

        # ---------------------------------
        # ⑥ 未匹配轨迹：missed + 1
        #    必须在⑤之前处理，
        #    因为⑤会往self.tracks里追加元素，
        #    下标会错位
        # ---------------------------------
        for track_index in unmatched_tracks:
            self.tracks[track_index].mark_missed()

        # ---------------------------------
        # ⑤ 未匹配检测：创建新轨迹
        # ---------------------------------
        for detection_index in unmatched_detections:
            new_track=Track(
                detections[detection_index],
                self.next_id
            )
            self.tracks.append(new_track)
            self.next_id+=1

        # ---------------------------------
        # ⑦ missed超过max_age：删除轨迹
        # ---------------------------------
        self.tracks=[
            track
            for track in self.tracks
            if not track.is_deleted(self.max_age)
        ]

        return self.tracks