# Air Doodle - Computer Vision Drawing Application

## About the Project
Air Doodle is an interactive computer vision application that allows users to draw on their computer screen in real-time using only hand gestures. By utilizing a standard webcam, the software tracks the user's hand movements and translates them into digital brush strokes. 

This project demonstrates practical skills in computer vision, real-time data processing, human-computer interaction (HCI), and state management in Python.

## Key Features
* **Touchless Drawing:** Draw freely on the screen by moving your index finger in the air.
* **Gesture Recognition:** The application recognizes specific hand poses to trigger different actions without the need for a keyboard or mouse.
* **Action History (Undo):** The system stores stroke history, allowing users to easily erase their last action using a simple fist gesture.
* **Virtual User Interface:** Features a modern, translucent interactive menu overlaid on the camera feed. Users can change brush colors by hovering over virtual buttons.
* **Motion Smoothing:** Implements a Kalman Filter to reduce camera jitter and ensure smooth, natural-looking drawing lines.

## Technologies Used
* **Python 3:** Core programming language.
* **OpenCV:** Used for image processing, rendering the digital canvas, and handling the webcam feed.
* **MediaPipe:** Google's framework used for robust, real-time hand and finger landmark tracking.
* **NumPy:** Utilized for efficient matrix operations and handling pixel data arrays.

## How to Use (Gesture Guide)
The application is entirely controlled via the right or left hand:
* **To Draw:** Raise only your index finger and move it across the camera's view. 
* **To Stop Drawing:** Open your hand completely or drop your index finger. The stroke will be saved to the canvas.
* **To Undo:** Make a closed fist. This will delete the last drawn line.
* **To Change Color:** Raise your index and middle fingers (peace sign) and move your hand to the top of the screen over the desired color on the virtual palette.

## Installation and Setup

**Prerequisites:**
Ensure Python 3.8 or higher is installed on your system.

**1. Install Dependencies:**
Open your terminal or command prompt and run the following command to install the required libraries:
`pip install opencv-python mediapipe numpy`

**2. Run the Application:**
Navigate to the project folder and execute the main script:
`python main.py`

**3. Exit:**
To close the application, press the 'q' key on your keyboard.

## Project Structure
The code is modular and organized using Object-Oriented Programming (OOP) principles for maintainability:
* `main.py`: The entry point that initializes the camera, UI, and main application loop.
* `hand_tracker.py`: Wraps the MediaPipe library to handle hand detection and landmark extraction.
* `gesture_controller.py`: Analyzes hand landmarks to classify the current gesture (Draw, Erase, UI).
* `drawing_manager.py`: Manages the canvas state, including the undo/redo stack and rendering lines.
* `kalman_filter.py`: Applies mathematical smoothing to the coordinate data to prevent jagged lines.
