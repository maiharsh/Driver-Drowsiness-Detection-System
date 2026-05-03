# Driver Drowsiness Detection System

## Overview

This project is a real-time Driver Drowsiness Detection System developed using Python, OpenCV, and MediaPipe. It monitors a driver's eye movements through a webcam feed and detects signs of drowsiness based on the Eye Aspect Ratio (EAR) method.

When prolonged eye closure is detected beyond a predefined threshold, the system triggers an alert to warn the driver and help prevent accidents caused by fatigue.

The project demonstrates practical implementation of computer vision and facial landmark detection for a real-world safety application.



## Features

- Real-time face and eye detection using webcam input
- Eye Aspect Ratio (EAR) based drowsiness monitoring
- Automatic drowsiness alert generation
- Facial landmark tracking using MediaPipe Face Mesh
- Lightweight and efficient implementation suitable for real-time use



## Technologies Used

- Python 3.12.9
- OpenCV
- MediaPipe 0.10.4
- NumPy
- SciPy
- winsound



## Working Principle

The system captures live video frames through a webcam and processes each frame to detect facial landmarks.

Using MediaPipe Face Mesh, eye landmark coordinates are extracted. These landmarks are used to calculate the Eye Aspect Ratio (EAR), which measures whether the eyes are open or closed.

- If EAR remains above the threshold, the driver is considered alert.
- If EAR falls below the threshold continuously for a certain number of frames, the system classifies it as drowsiness.
- An alarm is then triggered to alert the driver.

This approach helps reduce false alarms caused by normal blinking.



## Eye Aspect Ratio Formula

The Eye Aspect Ratio is computed as:

EAR = (||p2 - p6|| + ||p3 - p5||) / (2 * ||p1 - p4||)

Where:

- p1 to p6 represent eye landmark points
- Vertical distances measure eye opening
- Horizontal distance normalizes the ratio

A lower EAR indicates closed eyes.


## Project Structure

Driver-Drowsiness-Detection/
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore






## Future Improvements

Possible enhancements include:

- Yawn detection integration
- Mobile or embedded deployment
- Deep learning based drowsiness classification
- Integration with vehicle safety systems





## Limitations

- Performance depends on lighting conditions
- Accuracy may reduce if the face is partially occluded
- Webcam quality can affect landmark detection
- Threshold values may require tuning for different users

