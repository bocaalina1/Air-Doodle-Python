import cv2
import numpy as np

class KalmanSmoother:
    def __init__(self):
        self.kalman = cv2.KalmanFilter(4, 2)
        self.kalman.measurementMatrix = np.array([[1,0,0,0],
                                                  [0,1,0,0]], np.float32)

        self.kalman.transitionMatrix = np.array([[1,0,1,0],
                                                 [0,1,0,1],
                                                 [0,0,1,0],
                                                 [0,0,0,1]], np.float32)

        self.kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

    def smooth(self, x, y):
        measurement = np.array([[np.float32(x)],
                                [np.float32(y)]])
        self.kalman.correct(measurement)
        prediction = self.kalman.predict()
        return int(prediction[0]), int(prediction[1])
