# Hand Gesture PC Control

This project implements a computer vision-based system that allows users to control their PC using hand gestures captured through a webcam. It utilizes OpenCV, MediaPipe, and PyAutoGUI to interpret hand movements and translate them into mouse actions, scrolling, zooming, and even taking screenshots.

## Features

- Mouse control using index finger movement
- Left-click by bringing index finger and thumb together
- Right-click by bringing middle finger and thumb together
- Scrolling by moving the index finger up and down
- Zooming in/out using two-handed pinch gesture
- Taking screenshots by making a fist gesture

## Requirements

- Python 3.7+
- OpenCV
- MediaPipe
- PyAutoGUI

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/alf95/hand-gesture-pc-control.git
   cd hand-gesture-pc-control
   ```

2. Install the required packages:
   ```
   pip install opencv-python mediapipe pyautogui
   ```

## Usage

Run the script:

```
python hand_gesture_control.py
```

- Use your index finger to move the mouse cursor.
- Bring your index finger and thumb together to perform a left-click.
- Bring your middle finger and thumb together to perform a right-click.
- Move your index finger up and down to scroll.
- Use two hands, moving them apart or together, to zoom in or out.
- Make a fist to take a screenshot (saved as 'fist_screenshot.png').
- Press 'q' to quit the application.

## How it Works

1. The script captures video from the default webcam.
2. It uses MediaPipe to detect and track hand landmarks in each frame.
3. Based on the positions and movements of these landmarks, it interprets gestures:
   - The tip of the index finger controls mouse movement.
   - The distance between index finger and thumb triggers clicks.
   - Vertical movement of the index finger controls scrolling.
   - The distance between two hands controls zooming.
   - A fist gesture triggers a screenshot.
4. PyAutoGUI is used to control the mouse, perform clicks, scroll, and take screenshots based on the interpreted gestures.

## Customization

You can adjust various thresholds in the script to fine-tune the gesture recognition:

- `click_threshold`: Adjust the sensitivity for click detection.
- `scroll_threshold`: Change how much movement is needed to trigger scrolling.
- `screenshot_cooldown`: Modify the cooldown period between screenshots.
- `zoom_threshold`: Adjust the sensitivity for zoom gestures.

## Limitations

- The system requires good lighting conditions for accurate hand detection.
- It may not work well with complex backgrounds or multiple people in the frame.
- Gestures might take some practice to perform accurately.

## Contributing

Contributions to improve the project are welcome. Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- This project uses the MediaPipe library developed by Google.
- PyAutoGUI is used for simulating mouse and keyboard inputs.