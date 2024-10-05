# Virtual Keyboard with Hand Tracking

## Overview
This Python script creates a virtual keyboard that users can interact with by moving their hands. The program utilizes OpenCV for image capture, MediaPipe for hand tracking, and Pynput for simulating keyboard events. The script identifies hand gestures to press virtual keys displayed on the screen, allowing users to type text using their hand movements.

## Features
- **Virtual Keyboard**: A virtual keyboard displayed on the screen, allowing typing through hand gestures.
- **Hand Tracking**: Uses MediaPipe's hand tracking to detect the position of the user's hand.
- **Gesture Detection**: Detects hand gestures and correlates finger positions to simulate key presses.
- **Keyboard Interaction**: Includes common keys like `Q`, `W`, `E`, etc., as well as functional keys like `Backspace`, `Space`, and `Enter`.
- **Prolonged Press Detection**: Simulates prolonged key presses for typing when a hand remains on a button for more than 2 seconds.

## Prerequisites

- Python 3.x
- Required libraries:
  - `cv2` (OpenCV)
  - `mediapipe`
  - `pynput`
  - `math`
  - `time`

Install the required libraries using pip:

```bash
pip install opencv-python mediapipe pynput
```

## How It Works

1. **Hand Detection**: The script captures video from your webcam and uses MediaPipe to detect the position of your hands and fingers.
2. **Button Detection**: A grid of virtual buttons (keyboard keys) is drawn on the screen. Each button is associated with a specific key.
3. **Finger Position Mapping**: The position of the index and middle fingers are tracked. If the index finger is over a button, and the distance between the index and middle fingers is small, the key is "pressed."
4. **Prolonged Press**: If a key is held for more than 2 seconds, it will simulate typing the character or performing the associated function (e.g., backspace, space, enter).
5. **Final Text**: The typed text is displayed on the screen in real time.

## Running the Script

1. Connect your webcam.
2. Run the script:
   ```bash
   python virtual_keyboard.py
   ```
3. The program will display a virtual keyboard and start capturing hand movements. Use your hand to hover over the keys to "press" them.

4. Press `Esc` to exit the program.

## Customization

- **Keyboard Layout**: You can customize the `keys` list to change the layout of the virtual keyboard.
- **Button Size & Spacing**: The `button_width`, `button_height`, and `spacing` variables can be adjusted to modify the appearance of the buttons.

## Extracting Zipped Files

The project has been compressed using **7-Zip** into parts, each of 10 MB size, as shown in the image (e.g., `ai.zip.001`, `ai.zip.002`, etc.). To extract the files from these multiple parts after downloading them from GitHub, follow these steps:

1. **Download all parts**: Ensure you have downloaded all parts (e.g., `ai.zip.001`, `ai.zip.002`, and so on) from the GitHub repository.

2. **Install 7-Zip**: If you don't already have it, download and install 7-Zip from [here](https://www.7-zip.org/).

3. **Extract the files**:
   - Right-click on the first part (`ai.zip.001`).
   - Select **7-Zip > Extract Here** or **Extract to "ai.zip/"** (if you want to extract the contents into a separate folder).
   - 7-Zip will automatically combine all parts and extract the files.

4. **Move the Extracted Files**: After extracting the files:
   - **Cut and paste** the extracted `ai` folder into the **Virtual Keyboard** project folder, the one that contains the `.main` file. This ensures that the virtual keyboard can correctly access the extracted files and run smoothly.
 
