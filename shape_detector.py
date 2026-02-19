import cv2
import numpy as np

class ShapeDetector:

    def detect(self, contour):
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)

        if perimeter == 0:
            return "Unknown", contour

        circularity = (4 * np.pi * area) / (perimeter * perimeter)

        epsilon = 0.02 * perimeter
        approx = cv2.approxPolyDP(contour, epsilon, True)

        vertices = len(approx)

        if circularity > 0.75:
            return "Circle", approx
        elif vertices == 3:
            return "Triangle", approx
        elif vertices == 4:
            return "Rectangle", approx
        else:
            return "Polygon", approx
