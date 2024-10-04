import cv2
from pynput.keyboard import Controller, Key
import math
import time
import mediapipe as mp

# Define the keyboard and keys
keyboard = Controller()
keys = [["Q","W","E","R","T","Y","U","I","O","P"],
        ["A","S","D","F","G","H","J","K","L",";"],
        ["Z","X","C","V","B","N","M",",",".","/"]]
finalText = ""

# Define spacing and button dimensions
spacing = 10
button_width = 60
button_height = 60

# Define button class
class Button():
    def __init__(self, pos, text, size=[60, 60]):
        self.pos = pos
        self.text = text
        self.size = size

# Draw the buttons on the frame
def draw(img, buttonList):
    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), -1)
        
        # Calculate text size and position
        (text_w, text_h), _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2, 3)
        text_x = x + (w - text_w) // 2
        text_y = y + (h + text_h) // 2
        
        # Draw text
        cv2.putText(img, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3, cv2.LINE_AA)
    return img

# Initialize the button list
buttonList = []

# Add regular keys with spacing
for i in range(3):
    for j, key in enumerate(keys[i]):
        x = j * (button_width + spacing) + spacing
        y = i * (button_height + spacing) + spacing
        buttonList.append(Button([x, y], key))

# Add Backspace button
buttonList.append(Button([spacing, 3 * (button_height + spacing) + spacing], "Back", [100, button_height]))

# Add Space button
buttonList.append(Button([spacing + 110, 3 * (button_height + spacing) + spacing], "Space", [300, button_height]))

# Add Enter button
buttonList.append(Button([spacing + 420, 3 * (button_height + spacing) + spacing], "Enter", [100, button_height]))

# Initialize MediaPipe hands module
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

# Define the function to find hand landmarks
def findposition(frame):
    h, w, _ = frame.shape
    list = []
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for handLandmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, handLandmarks, mp_hands.HAND_CONNECTIONS)
            for id, pt in enumerate(handLandmarks.landmark):
                x = int(pt.x * w)
                y = int(pt.y * h)
                list.append([id, x, y])
    return list

# Start capturing video from the identified USB webcam index (assuming it's 0)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open video device.")
    exit()

# Variables to manage prolonged press
press_start_time = 0
pressing_button = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    frame = cv2.resize(frame, (840, 680))
    
    # Find hand positions
    positions = findposition(frame)
    frame = draw(frame, buttonList)
    
    if positions:
        for button in buttonList:
            x, y = button.pos
            w, h = button.size
            x1, y1 = positions[8][1], positions[8][2]
            x2, y2 = positions[12][1], positions[12][2]
            length = math.hypot(x2 - x1, y2 - y1)
            
            if x < x1 < x + w and y < y1 < y + h:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (122, 0, 122), -1)
                
                # Calculate text size and position
                (text_w, text_h), _ = cv2.getTextSize(button.text, cv2.FONT_HERSHEY_PLAIN, 2, 3)
                text_x = x + (w - text_w) // 2
                text_y = y + (h + text_h) // 2
                
                # Draw text
                cv2.putText(frame, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3, cv2.LINE_AA)
                
                print(f"Button {button.text} clicked, Length: {length}")

                # Check for prolonged press
                if pressing_button == button and time.time() - press_start_time > 2:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), -1)
                    cv2.putText(frame, button.text, (text_x, text_y), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 3, cv2.LINE_AA)
                    if button.text == "Back":
                        if finalText:  # Ensure there is something to delete
                            finalText = finalText[:-1]
                            keyboard.press(Key.backspace)
                            keyboard.release(Key.backspace)
                    elif button.text == "Enter":
                        finalText += "\n"
                        keyboard.press(Key.enter)
                        keyboard.release(Key.enter)
                    elif button.text == "Space":
                        finalText += " "
                        keyboard.press(' ')
                        keyboard.release(' ')
                    else:
                        finalText += button.text
                        keyboard.press(button.text)
                        keyboard.release(button.text)
                    pressing_button = None  # Reset after entering text
                    print(f"Updated finalText: {finalText}")

                elif pressing_button is None:
                    pressing_button = button
                    press_start_time = time.time()

            elif pressing_button == button:
                pressing_button = None  # Reset if moved out of button

    # Display the typed text
    cv2.rectangle(frame, (50, 350), (700, 450), (122, 0, 122), -1)
    cv2.putText(frame, finalText, (60, 425), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 3)
    
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == 27:  # Press 'Esc' to exit
        break

cap.release()
cv2.destroyAllWindows()
