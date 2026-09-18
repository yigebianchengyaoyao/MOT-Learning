from tracker.kalman_tracker import KalmanTracker


class Track:
    def __init__(self,bbox,track_id):

        #目标框
        self.bbox=bbox
        #目标ID
        self.id=track_id
        #存在多少帧
        self.age=1
        #连续多少帧没有匹配到检测框
        self.missed=0
        #每条轨迹自带一个卡尔曼滤波器，状态为[cx,cy,vx,vy]
        self.kalman=KalmanTracker(bbox)

    def predict(self):
        """
        ① 用Kalman预测下一帧位置。

        预测结果写回self.bbox，因此后续IoU计算用的是"预测框"，
        而不是"上一帧的检测框"。
        目标被遮挡、检测失败时，轨迹就靠这个预测框继续存在。
        """
        self.bbox=self.kalman.predict()
        return self.bbox

    def update(self,bbox):
        #当tracker成功匹配到新的检测框时调用
        """④ 匹配成功：用检测结果修正Kalman状态"""

        #用实际检测结果修正预测，同时更新框尺寸
        self.kalman.update(bbox)

        #匹配成功，位置以检测结果为准
        self.bbox=bbox
        self.age+=1
        self.missed=0

    def mark_missed(self):
        """⑥ 当前帧没有匹配到检测结果"""
        self.missed+=1

    def is_deleted(self,max_age):
        """
        ⑦ 判断轨迹是否应该删除。

        用 > 而不是 >=：max_age表示"最多容忍连续丢失多少帧"。
        """
        return self.missed>max_age