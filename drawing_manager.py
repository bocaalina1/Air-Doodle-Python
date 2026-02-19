import cv2
import numpy as np

class DrawingManager:
    def __init__(self, frame_shape):
        self.canvas = np.zeros(frame_shape, dtype=np.uint8)
        self.undo_stack = [] 
        self.redo_stack = []

   
    def add_stroke(self, points, color, thickness=4):
        stroke = {
            'points': np.array(points, dtype=np.int32),
            'color': color,
            'thickness': thickness
        }
        self.undo_stack.append(stroke)
        self.redo_stack.clear()
        self._redraw()

    def undo(self):
        if self.undo_stack:
            self.redo_stack.append(self.undo_stack.pop())
            self._redraw()

    def clear(self):
        self.undo_stack.clear()
        self.redo_stack.clear()
        self.canvas[:] = 0

    def _redraw(self):
        self.canvas[:] = 0
        for stroke in self.undo_stack:
            cv2.polylines(self.canvas, [stroke['points']], False, stroke['color'], stroke['thickness'])