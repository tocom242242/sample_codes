import cv2

cap = cv2.VideoCapture(0)

while(True):
    ret, frame = cap.read()
    cv2.imshow("frame", frame)

    cv2.imwrite("frame.jpg", frame)

    clipped_frame = frame[0:100, 0:100]
    cv2.imwrite("clipped_frame.jpg", clipped_frame)

    if cv2.waitKey(60) & 0xFF == ord('q'):
        break
