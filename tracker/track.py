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

    def update(self,bbox):
        #当tracker成功匹配到新的检测框时调用
        """更新目标位置"""

        self.bbox=bbox
        self.age+=1
        self.missed=0

    def mark_missed(self):
        """当前没有检测到目标"""
        self.missed+=1