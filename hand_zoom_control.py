import cv2
import mediapipe as mp
import pyautogui
import math

# Initialize MediaPipe Hands and OpenCV
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=2)  # Track both hands

# Access webcam
cap = cv2.VideoCapture(0)

# Threshold for zoom sensitivity
zoom_threshold = 0.02
prev_distance = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (MediaPipe uses RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Process the frame and get hand landmarks
    result = hands.process(rgb_frame)
    
    if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:
        # Get the landmarks for both hands
        hand_landmarks1 = result.multi_hand_landmarks[0]
        hand_landmarks2 = result.multi_hand_landmarks[1]
        
        # Extract the index finger tips from both hands (relative coordinates)
        index_tip1 = hand_landmarks1.landmark[8]
        index_tip2 = hand_landmarks2.landmark[8]
        
        # Log the relative positions before conversion
        print(f"Left hand (before conversion) index tip: x={index_tip1.x}, y={index_tip1.y}, z={index_tip1.z}")
        print(f"Right hand (before conversion) index tip: x={index_tip2.x}, y={index_tip2.y}, z={index_tip2.z}")
        
        # Convert landmarks to screen coordinates
        height, width, _ = frame.shape
        index_tip1_x = int(index_tip1.x * width)
        index_tip1_y = int(index_tip1.y * height)
        index_tip2_x = int(index_tip2.x * width)
        index_tip2_y = int(index_tip2.y * height)

        # Log the index finger positions after conversion
        print(f"Left hand (after conversion) index tip: ({index_tip1_x}, {index_tip1_y})")
        print(f"Right hand (after conversion) index tip: ({index_tip2_x}, {index_tip2_y})")

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
                elif distance < prev_distance:
                    pyautogui.hotkey('ctrl', '-')  # Zoom out

        # Update previous distance for next frame
        prev_distance = distance
    
    # Display the output
    cv2.imshow('Zoom with Hand Gestures', frame)
    
    # Break the loop with 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close windows
cap.release()
cv2.destroyAllWindows()
