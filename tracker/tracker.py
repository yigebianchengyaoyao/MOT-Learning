from tracker.track import Track
from tracker.simple_tracker import calculate_iou

class SimpleTracker:

    def __init__(self):
        #保存所有目标
        self.tracks=[]
        #下一个ID
        self.next_id=1


    def update(self,detections):
        """
                输入:
                detections:
                [
                    bbox1,
                    bbox2
                ]

                输出:
                当前所有目标
        """

        if len(self.tracks)==0:

            for det in detections:
                track=Track(det,self.next_id)
                self.tracks.append(track)
                self.next_id+=1

        else:
            #记录已经匹配的目标
            matched=[]
            for det in detections:
                best_iou=0
                best_track=None

                #寻找最大IoU目标
                for track in self.tracks:
                    iou=calculate_iou(det,track.bbox)

                    if iou>best_iou:
                        best_iou=iou
                        best_track=track

                #超过阈值认为同一个目标
                if best_iou>0.3:
                    best_track.update(det)
                    matched.append(best_track)
                else:
                    #创建新目标
                    new_track=Track(
                        det,
                        self.next_id
                    )

                    self.tracks.append(new_track)
                    self.next_id+=1

        return self.tracks
