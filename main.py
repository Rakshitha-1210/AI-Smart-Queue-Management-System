import cv2
import pyttsx3
import time

# -------------------------------
# Voice Engine
# -------------------------------
engine = pyttsx3.init()

# Voice speed
engine.setProperty('rate', 150)

# -------------------------------
# Human Detector
# -------------------------------
hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

# -------------------------------
# Open Webcam
# -------------------------------
cam = cv2.VideoCapture(0)

if not cam.isOpened():
    print("Camera not working")
    exit()

# -------------------------------
# Voice Timer
# -------------------------------
last_announcement = time.time()

# -------------------------------
# Main Loop
# -------------------------------
while True:

    ret, frame = cam.read()

    if not ret:
        print("Failed to capture frame")
        break

    # Resize Frame
    frame = cv2.resize(frame, (800, 600))

    # -------------------------------
    # Detect People
    # -------------------------------
    people, _ = hog.detectMultiScale(
        frame,
        winStride=(8, 8),
        padding=(8, 8),
        scale=1.05
    )

    count = 0

    # Draw Rectangles Around People
    for (x, y, w, h) in people:

        count += 1

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0,255,0),
            2
        )

    # -------------------------------
    # Waiting Time
    # -------------------------------
    wait_time = count * 2

    # -------------------------------
    # Queue Status
    # -------------------------------
    if count <= 3:
        status = "Normal"

    elif count <= 6:
        status = "Busy"

    else:
        status = "Overcrowded"

    # -------------------------------
    # Counter Recommendation
    # -------------------------------
    if count > 5:
        recommendation = "Move to Next Counter"
    else:
        recommendation = "No Need to Move"

    # -------------------------------
    # Voice Announcement Every 10 Sec
    # -------------------------------
    current_time = time.time()

    if current_time - last_announcement > 10:

        voice_msg = (
            f"There are {count} people in the queue. "
            f"Estimated waiting time is {wait_time} minutes. "
            f"Queue status is {status}. "
            f"{recommendation}"
        )

        engine.say(voice_msg)
        engine.runAndWait()

        last_announcement = current_time

    # -------------------------------
    # Display Information
    # -------------------------------
    cv2.putText(
        frame,
        f"People Count: {count}",
        (20,40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255,0,0),
        2
    )

    cv2.putText(
        frame,
        f"Waiting Time: {wait_time} mins",
        (20,80),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,0,255),
        2
    )

    cv2.putText(
        frame,
        f"Queue Status: {status}",
        (20,120),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,255),
        2
    )

    cv2.putText(
        frame,
        recommendation,
        (20,160),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0,255,0),
        2
    )

    # -------------------------------
    # Show Output Window
    # -------------------------------
    cv2.imshow(
        "AI Smart Queue Management System",
        frame
    )

    # ESC Key to Exit
    if cv2.waitKey(1) == 27:
        break

# -------------------------------
# Release Camera
# -------------------------------
cam.release()
cv2.destroyAllWindows()