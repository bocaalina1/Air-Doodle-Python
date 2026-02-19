import cv2
import numpy as np
import time

# Custom modules
from hand_tracker import HandTracker
from kalman_filter import KalmanSmoother
from drawing_manager import DrawingManager
from gesture_controller import GestureController

# --- CONFIGURATION ---
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Pastel Colors (BGR Format)
COLORS = [
    (80, 80, 255),    # Coral Red
    (255, 191, 0),    # Deep Sky Blue
    (0, 215, 255),    # Golden Yellow
    (147, 20, 255),   # Purple/Pink
    (50, 205, 50),    # Lime Green
]

def main():
    # Initialize Camera
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)

    # Initialize Modules
    tracker = HandTracker()
    smoother = KalmanSmoother()
    gesture = GestureController()
    
    # Note: ShapeDetector is no longer needed for doodling

    success, frame = cap.read()
    if not success:
        print("Error: Camera not found")
        return

    # Initialize Drawing Manager
    drawing = DrawingManager(frame.shape)

    # State Variables
    current_stroke = []         # Temporary list for the line currently being drawn
    is_drawing = False          # Flag to track drawing state
    selected_color = COLORS[0]
    
    prev_time = 0
    last_undo_time = 0
    UNDO_COOLDOWN = 0.5         # Seconds to wait between undo actions

    current_action_text = "Ready to Doodle"

    while True:
        success, frame = cap.read()
        if not success: break
        
        # Mirror the frame
        frame = cv2.flip(frame, 1)

        current_action_text = "Move hand to start"
        
        results = tracker.process(frame)

        # EDGE CASE: If hand leaves the frame while drawing, save the stroke
        if not results.multi_hand_landmarks and is_drawing:
            is_drawing = False
            if len(current_stroke) > 1:
                drawing.add_stroke(current_stroke, selected_color)
            current_stroke = []

        if results.multi_hand_landmarks:
            for i, hand in enumerate(results.multi_hand_landmarks):
                lm = hand.landmark
                h, w, _ = frame.shape

                # 1. Identify Gesture
                gesture_type = gesture.get_gesture(lm, tracker)

                # 2. Get Coordinates (Index Finger Tip)
                ix = int(lm[8].x * w)
                iy = int(lm[8].y * h)
                # Smooth the movement
                ix, iy = smoother.smooth(ix, iy)

                # --- DOODLING LOGIC ---

                # CASE 1: DRAWING (Index finger up)
                if gesture_type == "DRAW":
                    current_action_text = "DOODLING..."
                    is_drawing = True
                    current_stroke.append((ix, iy))
                    
                    # Draw the temporary line (live feedback)
                    if len(current_stroke) > 1:
                        # Draw directly on the frame
                        cv2.polylines(frame, [np.array(current_stroke, np.int32)], False, selected_color, 4)
                    
                    # Draw visual cursor
                    cv2.circle(frame, (ix, iy), 5, selected_color, -1)

                # CASE 2: STOP DRAWING (Any other gesture)
                else:
                    # If we were drawing and just stopped, save the stroke
                    if is_drawing:
                        is_drawing = False
                        if len(current_stroke) > 1:
                            drawing.add_stroke(current_stroke, selected_color)
                        current_stroke = [] # Reset

                    # Handle other gestures (Undo, Colors)
                    
                    if gesture_type == "ERASE": # Fist
                        current_action_text = "ERASE (Undo)"
                        if time.time() - last_undo_time > UNDO_COOLDOWN:
                            drawing.undo()
                            last_undo_time = time.time()
                            # Visual feedback for undo
                            cv2.circle(frame, (ix, iy), 20, (0,0,255), -1)

                    elif gesture_type == "UI": # Two fingers
                        current_action_text = "COLOR SELECT"
                        if iy < 80: # Top menu area
                            idx = ix // 100
                            if idx < len(COLORS):
                                selected_color = COLORS[idx]
                                current_action_text = "Color Changed!"

                tracker.draw_landmarks(frame, hand)

        # --- MERGE CANVAS + FRAME ---
        # 1. Get the permanent canvas
        canvas_gray = cv2.cvtColor(drawing.canvas, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(canvas_gray, 1, 255, cv2.THRESH_BINARY)
        mask_inv = cv2.bitwise_not(mask)
        
        # Mask out the drawing area on the original frame
        frame = cv2.bitwise_and(frame, frame, mask=mask_inv)
        # Add the colored drawing
        frame = cv2.add(frame, drawing.canvas)

        # --- UI OVERLAY ---
        ui_overlay = frame.copy()
        
        # Draw Palette
        for j, color in enumerate(COLORS):
            cv2.rectangle(ui_overlay, (j*100, 0), (j*100+100, 80), color, -1)
            if color == selected_color:
                cv2.rectangle(ui_overlay, (j*100, 0), (j*100+100, 80), (255,255,255), 4)

        # Draw Status Bar
        cv2.rectangle(ui_overlay, (0, 80), (FRAME_WIDTH, 120), (30,30,30), -1)
        
        # Apply Transparency
        cv2.addWeighted(ui_overlay, 0.6, frame, 0.4, 0, frame)

        # Draw Text
        cv2.putText(frame, current_action_text, (20, 108), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2, cv2.LINE_AA)
        
        # Draw FPS
        curr_time = time.time()
        fps = 1 / (curr_time - prev_time) if prev_time else 0
        prev_time = curr_time
        cv2.putText(frame, f"FPS: {int(fps)}", (FRAME_WIDTH-120, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 2)

        cv2.imshow("Air Doodle", frame)
        if cv2.waitKey(1) == ord('q'): break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()