import cv2
import mediapipe as mp
import pyautogui
import math
import time

# Initialize MediaPipe Hands and OpenCV
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2)  # Track two hands for zoom functionality

# Access webcam
cap = cv2.VideoCapture(0)

# Get screen size for mouse control
screen_width, screen_height = pyautogui.size()

# Thresholds
click_threshold = 0.03  # Distance between thumb and index finger for clicking
scroll_threshold = 20    # Amount of movement for scrolling
screenshot_cooldown = 2   # Time in seconds to avoid multiple screenshots in quick succession
last_screenshot_time = 0  # Timestamp of the last screenshot taken
zoom_threshold = 0.02     # Sensitivity for zoom gestures
prev_distance = None      # For zoom tracking
prev_y = None  # For scrolling


def get_distance(p1, p2):
    """ Calculate the Euclidean distance between two landmarks (p1 and p2). """
    return math.sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def is_fist(hand_landmarks):
    """
    Enhanced detection to check if the hand is forming a fist.
    All finger tips (index, middle, ring, pinky) should be near their respective PIP joints, 
    and the thumb should be tucked in near the palm.
    """
    finger_tip_ids = [8, 12, 16, 20]  # Index, middle, ring, and pinky tips
    finger_pip_ids = [6, 10, 14, 18]  # PIP joints for index, middle, ring, and pinky
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[2]  # Thumb MCP joint (closer to the palm)

    # Check if all fingers are curled by comparing tip positions to PIP joints
    for tip_id, pip_id in zip(finger_tip_ids, finger_pip_ids):
        if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[pip_id].y:
            return False  # Not a fist if any fingertip is above its PIP joint

    # Ensure thumb is tucked in (tip closer to palm)
    if thumb_tip.x > thumb_ip.x:
        return False  # Thumb should be curled inward toward the palm

    return True


while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)

    # Convert the frame to RGB (MediaPipe uses RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame and get hand landmarks
    result = hands.process(rgb_frame)

    if result.multi_hand_landmarks:
        if len(result.multi_hand_landmarks) == 2:
            # If two hands are detected, disable mouse control and enable zoom functionality
            hand_landmarks1 = result.multi_hand_landmarks[0]
            hand_landmarks2 = result.multi_hand_landmarks[1]

            # Extract the index finger tips from both hands
            index_tip1 = hand_landmarks1.landmark[8]
            index_tip2 = hand_landmarks2.landmark[8]

            # Convert landmarks to screen coordinates
            height, width, _ = frame.shape
            index_tip1_x = int(index_tip1.x * width)
            index_tip1_y = int(index_tip1.y * height)
            index_tip2_x = int(index_tip2.x * width)
            index_tip2_y = int(index_tip2.y * height)

            # Draw landmarks on the hands
            mp_drawing.draw_landmarks(frame, hand_landmarks1, mp_hands.HAND_CONNECTIONS)
            mp_drawing.draw_landmarks(frame, hand_landmarks2, mp_hands.HAND_CONNECTIONS)

            # Calculate the Euclidean distance between both index finger tips
            distance = math.sqrt((index_tip2_x - index_tip1_x) ** 2 + (index_tip2_y - index_tip1_y) ** 2)

            if prev_distance is not None:
                # Compare current distance to previous distance to detect zoom
                if abs(distance - prev_distance) > zoom_threshold * width:
                    if distance > prev_distance:
                        pyautogui.hotkey('ctrl', '+')  # Zoom in
                        print("Zooming In")
                    elif distance < prev_distance:
                        pyautogui.hotkey('ctrl', '-')  # Zoom out
                        print("Zooming Out")

            # Update previous distance for next frame
            prev_distance = distance

        else:
            # Single hand detected, allow mouse control, clicking, and scrolling
            hand_landmarks = result.multi_hand_landmarks[0]

            # Extract landmark positions (index finger tip, thumb tip, middle finger tip)
            index_tip = hand_landmarks.landmark[8]
            thumb_tip = hand_landmarks.landmark[4]
            middle_tip = hand_landmarks.landmark[12]

            # Convert the index finger tip position to screen coordinates (for mouse movement)
            height, width, _ = frame.shape
            index_tip_x = int(index_tip.x * width)
            index_tip_y = int(index_tip.y * height)

            # Move the mouse to the corresponding screen coordinates
            mouse_x = int(index_tip.x * screen_width)
            mouse_y = int(index_tip.y * screen_height)
            pyautogui.moveTo(mouse_x, mouse_y)

            # Calculate the distance between index finger and thumb (for left click)
            click_distance = get_distance(index_tip, thumb_tip)

            # Detect left click (index and thumb close together)
            if click_distance < click_threshold:
                pyautogui.click()

            # Calculate the distance between middle finger and thumb (for right click)
            right_click_distance = get_distance(middle_tip, thumb_tip)

            # Detect right click (middle and thumb close together)
            if right_click_distance < click_threshold:
                pyautogui.click(button='right')

            # Scrolling: Detect the vertical movement of the index finger
            if prev_y is not None:
                dy = index_tip_y - prev_y
                if abs(dy) > scroll_threshold:
                    pyautogui.scroll(-int(dy))

            # Update previous Y position for scrolling
            prev_y = index_tip_y

            # Check if the hand is forming a fist for screenshot
            if is_fist(hand_landmarks):
                current_time = time.time()
                if (current_time - last_screenshot_time) > screenshot_cooldown:
                    # Take a screenshot
                    screenshot = pyautogui.screenshot()
                    screenshot.save('fist_screenshot.png')
                    print("Screenshot taken with a fist!")
                    last_screenshot_time = current_time

        # Draw landmarks on the hand
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the output
    cv2.imshow('PC Control with Hand Gestures', frame)

    # Break the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
