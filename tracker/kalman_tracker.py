import cv2
import numpy as np

class KalmanTracker:
    def __init__(self,bbox):
        """
        bbox格式：
        [x1, y1, x2, y2]
        """
        self.kf=cv2.KalmanFilter(4,2)
        self.kf.transitionMatrix=np.array(
            [
                [1, 0, 1, 0],
                [0, 1, 0, 1],
                [0, 0, 1, 0],
                [0, 0, 0, 1]
            ],
            dtype=np.float32
        )

        self.kf.measurementMatrix=np.array(
            [
                [1, 0, 0, 0],
                [0, 1, 0, 0]
            ],
            dtype=np.float32
        )

        #过程噪声
        self.kf.processNoiseCov=(
            np.eye(4,dtype=np.float32)*0.03
        )

        #测量噪声
        self.kf.measurementNoiseCov=(
            np.eye(2,dtype=np.float32)*1
        )
        # 后验误差协方差
        # OpenCV默认errorCovPost全为0，会把卡尔曼增益压到接近0，
        # 滤波器几乎不采信检测结果，表现为"预测严重滞后、速度要很多帧才估计出来"。
        # 这里初始化为较大值，表示"一开始对目标状态完全不确定"。
        self.kf.errorCovPost = (
                np.eye(4, dtype=np.float32) * 10
        )

        x1,y1,x2,y2=bbox
        cx=(x1+x2)/2
        cy=(y1+y2)/2

        #初始化kalman状态
        self.kf.statePost=np.array(
            [
                [cx],
                [cy],
                [0],
                [0]
            ],
            dtype=np.float32
        )

        #保存框尺寸
        self.width=x2-x1
        self.height=y2-y1

    def predict(self):
        """预测下一帧目标位置"""
        prediction=self.kf.predict()
        cx=prediction[0,0]
        cy=prediction[1,0]

        #中心点重新转换bbox
        x1=cx-self.width/2
        y1=cy-self.height/2
        x2=cx+self.width/2
        y2=cy+self.height/2

        return [x1,y1,x2,y2]

    def update(self,bbox):
        """使用yolo检测结果修正kalman状态"""
        x1,y1,x2,y2=bbox
        cx=(x1+x2)/2
        cy=(y1+y2)/2

        measurement=np.array(
            [
                [cx],
                [cy]
            ],
            dtype=np.float32
        )

        #使用实际检测结果修正预测
        self.kf.correct(measurement)
        #更新目标框尺寸
        self.width=x2-x1
        self.height=y2-y1