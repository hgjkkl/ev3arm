import cv2
from cvzone.HandTrackingModule import HandDetector
from pandas import to_numeric
import ev3_dc as ev3

my_ev3 = ev3.EV3(protocol=ev3.WIFI, host='00:16:53:4D:AB:AE')
motorX = ev3.Motor(ev3.PORT_B, ev3_obj=my_ev3)
motorY = ev3.Motor(ev3.PORT_C, ev3_obj=my_ev3)
motorC = ev3.Motor(ev3.PORT_D, ev3_obj=my_ev3)
motorX.sync_mode = ev3.STD
motorY.sync_mode = ev3.STD
motorC.sync_mode = ev3.STD

cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

previousFrame = 0

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)  # Draw hand
    fps = cap.get(cv2.CAP_PROP_FPS)  # FPS counter
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)  # Camera feed width
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)  # Camera feed height
    print(width, height, fps)

    if hands:
        hand1 = hands[0]
        centerPoint1 = hand1["center"]  # Center of the hand cx,cy
        fingers1 = detector.fingersUp(hand1)  # Number of fingers up/down
        cpX = centerPoint1[0]
        cpY = centerPoint1[1]
        currentX = int(-1.25 * cpX)
        print(sum(fingers1), cpX, cpY, round(int(-1.25*cpX), -2))

    # Movement definitions
        movement_open_C = (
            motorC.move_to(-80) +
            motorC.stop_as_task(brake=False)
        )
        movement_close_C = (
            motorC.move_to(-10) +
            motorC.stop_as_task(brake=False)
        )

        movement_sync_X = (
            motorX.move_to(round(int(-1.25*cpX), -1), speed=25) +
            motorX.stop_as_task(brake=True)
        )
        movement_Y_down = (
                motorY.move_to(-20, speed=25) +
                motorY.stop_as_task(brake=False)
        )

        if sum(fingers1) == 5:
            movement_open_C.start()
            movement_open_C.join()
        elif sum(fingers1) == 0:
            movement_close_C.start()
            movement_close_C.join()

        if cpY <= 300:
            motorY.start_move(direction=-1, speed=25)
        else:
            motorY.stop()
            movement_Y_down.start()
            movement_Y_down.join()

        if round(int(-1.25*cpX), -2) != round(to_numeric(motorX.position), -2):
            movement_sync_X.start()
            movement_sync_X.join()

    cv2.imshow("Camera", img)
    cv2.waitKey(1)
    if cv2.getWindowProperty('Camera', cv2.WND_PROP_VISIBLE) < 1:
        break
motorY.stop()
motorX.stop()
motorC.stop()
cv2.destroyAllWindows()