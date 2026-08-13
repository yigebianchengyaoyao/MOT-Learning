class Track:
    def __init__(self,bbox,track_id):

        #目标框
        self.bbox=bbox
        #目标ID
        self.id=track_id
        #存在多少帧
        self.age=1

    def update(self,bbox):

        """更新目标位置"""

        self.bbox=bbox
        self.age+=1