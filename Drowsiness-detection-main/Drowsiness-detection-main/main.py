import cv2
import mediapipe as mp
import numpy as np
from scipy.spatial import distance as dist
import winsound

# ---------------- CONFIG ---------------- #

EYE_AR_THRESH = 0.20
EYE_AR_CONSEC_FRAMES = 20

# ---------------- MEDIAPIPE INIT ---------------- #

mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

face_mesh = mp_face_mesh.FaceMesh(
    refine_landmarks=True,
    max_num_faces=1
)

# ---------------- EAR FUNCTION ---------------- #

def calculate_ear(eye_points, facial_landmarks):
    
    coords = []

    for index in eye_points:
        landmark = facial_landmarks.landmark[index]
        coords.append(np.array([landmark.x, landmark.y]))

    # Vertical distances
    v1 = dist.euclidean(coords[1], coords[5])
    v2 = dist.euclidean(coords[2], coords[4])

    # Horizontal distance
    h = dist.euclidean(coords[0], coords[3])

    ear = (v1 + v2) / (2.0 * h)

    return ear


# Eye landmark indices
LEFT_EYE = [33,160,158,133,153,144]
RIGHT_EYE = [362,385,387,263,373,380]

# Counter
COUNTER = 0

# Webcam
cap = cv2.VideoCapture(0)

print("System Running... Press ESC to exit.")

# ---------------- MAIN LOOP ---------------- #

while cap.isOpened():

    ret, frame = cap.read()

    if not ret:
        break

    # Mirror view
    frame = cv2.flip(frame,1)

    rgb_frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)

    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:

        for face_landmarks in results.multi_face_landmarks:

            # -------- DRAW FACE MESH -------- #

            mp_drawing.draw_landmarks(
                image=frame,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(
                    color=(255,200,100),  # Ice blue (BGR format)
                    thickness=1
                )
            )

            # -------- DRAW EAR POINTS -------- #

            h,w,_ = frame.shape

            for idx in LEFT_EYE + RIGHT_EYE:

                landmark = face_landmarks.landmark[idx]

                x = int(landmark.x * w)
                y = int(landmark.y * h)

                cv2.circle(
                    frame,
                    (x,y),
                    3,
                    (255,0,0),
                    -1
                )

            # -------- EAR CALCULATION -------- #

            left_ear = calculate_ear(
                LEFT_EYE,
                face_landmarks
            )

            right_ear = calculate_ear(
                RIGHT_EYE,
                face_landmarks
            )

            avg_ear = (left_ear + right_ear)/2.0

            # -------- DROWSINESS LOGIC -------- #

            if avg_ear < EYE_AR_THRESH:

                COUNTER += 1

                if COUNTER >= EYE_AR_CONSEC_FRAMES:

                    status = "DROWSY ALERT!"
                    color = (0,0,255)

                    winsound.Beep(1000,200)

                else:

                    status = "Eyes Closing..."
                    color = (0,165,255)

            else:

                COUNTER = 0
                status = "Eyes Open"
                color = (0,255,0)

            # -------- DISPLAY INFO -------- #

            cv2.putText(
                frame,
                f"EAR: {avg_ear:.2f}",
                (30,40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2
            )

            cv2.putText(
                frame,
                status,
                (30,75),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                color,
                2
            )

            cv2.putText(
                frame,
                f"Counter: {COUNTER}",
                (30,110),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                color,
                2
            )

    cv2.imshow(
        "Driver Drowsiness Detection System",
        frame
    )

    if cv2.waitKey(1)==27:
        break

# ---------------- CLEANUP ---------------- #

cap.release()
cv2.destroyAllWindows()