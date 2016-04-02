import share_var
import HandsOn
import threading
import serial
from pymouse import PyMouse
from pykeyboard import PyKeyboard

def mouseControl():
    """ Control the mouse using glove accelerometer """

    m = PyMouse()
    x_dim,y_dim = m.screen_size()
    m.move(x_dim/2,y_dim/2)

    while True:
        x_pos = (x_dim/2) + int(-share_var.yaw*x_dim/90.0)
        y_pos = (y_dim/2) + int(-share_var.pitch*y_dim/90.0)

        # if (x_pos < 0): x_pos = 0
        # if (x_pos > x_dim): x_pos = x_dim
        # if (y_pos < 0): y_pos = 0
        # if (y_pos > y_dim): y_pos = y_dim

        m.move(x_pos, y_pos)
## end mouseControl

def arrowControl():
    """ Control arrow keys using glove accelerometer """

    k = PyKeyboard()
    left_pressed = right_pressed = up_pressed = down_pressed = key_pressed = False

    while True:
        left = (share_var.roll > 25.0)
        right = (share_var.roll < -30.0)
        up = (share_var.pitch > 25.0)
        down = (share_var.pitch < -30.0)

        if left:
            if not(left_pressed or key_pressed):
                k.press_key(k.left_key)
                left_pressed = True
                key_pressed = True
        else:
            if left_pressed:
                k.release_key(k.left_key)
                left_pressed = False
                key_pressed = False
        if right:
            if not(right_pressed or key_pressed):
                k.press_key(k.right_key)
                right_pressed = True
                key_pressed = True
        else:
            if right_pressed:
                k.release_key(k.right_key)
                right_pressed = False
                key_pressed = False
        # if up:
        #     if not(up_pressed or key_pressed):
        #         k.press_key(k.up_key)
        #         up_pressed = True
        #         key_pressed = True
        # else:
        #     if up_pressed:
        #         k.release_key(k.up_key)
        #         up_pressed = False
        #         key_pressed = False
        # if down:
        #     if not(down_pressed or key_pressed):
        #         k.press_key(k.down_key)
        #         down_pressed = True
        #         key_pressed = True
        # else:
        #     if down_pressed:
        #         k.release_key(k.down_key)
        #         down_pressed = False
        #         key_pressed = False


def main():

    ser = serial.Serial('/dev/ttyACM0', 9600) #Bhavesh's PORT
    serialThread = threading.Thread(target=HandsOn.parseSerialHandData, args=(ser,))
    serialThread.setDaemon(True)
    serialThread.start()

    mouseThread = threading.Thread(target=mouseControl)
    mouseThread.setDaemon(True)
    mouseThread.start()

    while True:
        pass

if __name__ == "__main__":
    main()
