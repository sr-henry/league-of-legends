import cv2
import numpy as np

def nothing(x):
    pass

cv2.namedWindow("frame")

cv2.createTrackbar("L-B", "frame", 0, 255, nothing)
cv2.createTrackbar("L-G", "frame", 0, 255, nothing)
cv2.createTrackbar("L-R", "frame", 0, 255, nothing)
cv2.createTrackbar("U-B", "frame", 0, 255, nothing)
cv2.createTrackbar("U-G", "frame", 0, 255, nothing)
cv2.createTrackbar("U-R", "frame", 0, 255, nothing)


frame = cv2.imread("teste.jpeg")

cv2.imshow("window", frame)

while True:

    lb = cv2.getTrackbarPos("L-B", "frame")
    lg = cv2.getTrackbarPos("L-G", "frame")
    lr = cv2.getTrackbarPos("L-R", "frame")
    
    ub = cv2.getTrackbarPos("U-B", "frame")
    ug = cv2.getTrackbarPos("U-G", "frame")
    ur = cv2.getTrackbarPos("U-R", "frame")

    lower = np.array([lr, lg, lb])
    upper = np.array([ur, ug, ub])

    print(upper)

    mask = cv2.inRange(frame, lower, upper)

    cv2.imshow("mask", mask)

    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()