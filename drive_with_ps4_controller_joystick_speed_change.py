import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

import asyncio

from sphero_sdk import SerialAsyncDal
from sphero_sdk import SpheroRvrAsync
from pyPS4Controller.controller import Controller

# initialize global constants
JOYSTICK_THRESHOLD = 10000
SPEED_INCREMENT    = 64

# initialize global variables
speed = 0
heading = 0
heading_active_left = False
heading_active_right = False
flags = 0

def shutdown_callback():
    os.system("sudo shutdown -h now")

def my_sequences():
    return [
        {"inputs": ['square', 'square', 'circle', 'circle', 'square', 'circle', 'square', 'circle'],
         "callback": shutdown_callback}
    ]

class MyController(Controller):

    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("Forward")
        global speed
        global speed_change
        global flags
        speed = speed + SPEED_INCREMENT
        flags = 0

        speed_change = True

    def on_x_release(self):
        print("Stop")
        global speed
        global speed_change
        speed = speed - SPEED_INCREMENT
        speed_change = True

    def on_left_arrow_press(self):
        print("Turning left")
        global heading_active_left
        heading_active_left = True

    def on_right_arrow_press(self):
        print("Turning right")
        global heading_active_right
        heading_active_right = True

    def on_left_right_arrow_release(self):
        print("Stop turning")
        global heading_active_left
        global heading_active_right
        heading_active_left = False
        heading_active_right = False

    def on_L3_up(self, value):
        global speed
        global speed_change
        global flags

        if value < -1 * JOYSTICK_THRESHOLD:
            print("Forward")
            speed = SPEED_INCREMENT
            flags = 0
        else:
            print("Stop")
            speed = 0

        speed_change = True

    def on_L3_down(self, value):
        global speed
        global speed_change
        global flags

        if value > JOYSTICK_THRESHOLD:
            print("Backward")
            speed = SPEED_INCREMENT
            flags = 1
        else:
            print("Stop")
            speed = 0

        speed_change = True

    def on_L3_y_at_rest(self):
        print("Stop")
        global speed
        global speed_change
        speed = 0
        speed_change = True

    # def on_L3_left(self, value):
    #     global heading_active_left
    #     if value < -20000:
    #         print("Turning left")
    #         heading_active_left = True
    #     else:
    #         print("Stop turning")
    #         heading_active_left = False

    # def on_L3_right(self, value):
    #     global heading_active_right
    #     if value > 20000:
    #         print("Turning right")
    #         heading_active_right = True
    #     else:
    #         print("Stop turning")
    #         heading_active_right = False

    # def on_L3_x_at_rest(self):
    #     print("Stop turning")
    #     global heading_active_left
    #     global heading_active_right
    #     heading_active_left = False
    #     heading_active_right = False

    def on_R3_left(self, value):
        global heading_active_left

        if value < -1 * JOYSTICK_THRESHOLD:
            print("Turning left")
            heading_active_left = True
        else:
            print("Stop turning left")
            heading_active_left = False

    def on_R3_right(self, value):
        global heading_active_right

        if value > JOYSTICK_THRESHOLD:
            print("Turning right")
            heading_active_right = True
        else:
            print("Stop turning right")
            heading_active_right = False

    def on_R3_x_at_rest(self):
        print("Stop turning")
        global heading_active_left
        global heading_active_right
        heading_active_left = False
        heading_active_right = False

loop = asyncio.get_event_loop()
rvr = SpheroRvrAsync(
    dal=SerialAsyncDal(
        loop
    )
)

async def main():

    global speed
    global heading
    global flags
    global heading_active_left
    global heading_active_right
    global speed_change

    speed_change = False

    await rvr.wake()

    await rvr.reset_yaw()

    while True:
        if heading_active_left:
            heading -= 10
        elif heading_active_right:
            heading += 10

        # check the speed value, and wrap as necessary.
        if speed > 255:
            speed = 255
        elif speed < -255:
            speed = -255

        # check the heading value, and wrap as necessary.
        if heading > 359:
            heading = heading - 359
        elif heading < 0:
            heading = 359 + heading

        if heading_active_left or heading_active_right or speed_change:
            speed_change = False

            # issue the driving command
            await rvr.drive_with_heading(speed, heading, flags)

            # sleep the infinite loop for a 10th of a second to avoid flooding the serial port.
            await asyncio.sleep(0.01)


def run_loop():
    global loop
    loop.run_until_complete(
        asyncio.gather(
            main()
        )
    )

if __name__ == "__main__":
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)

    loop.run_in_executor(None, lambda: controller.listen(timeout=1000, on_sequence=my_sequences()))

    try:
        run_loop()
    except KeyboardInterrupt:
        print("Keyboard Interrupt...")
    finally:
        print("Press any key to exit.")
        exit(1)
