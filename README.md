# sphero-tinker
Example usage of the [sphero-inc/sphero-sdk-raspberrypi-python](https://github.com/sphero-inc/sphero-sdk-raspberrypi-python) framework with a Sphero RVR: navigation control with a PS4 Controller.
- To pair the controller: https://bluedot.readthedocs.io/en/latest/pairpipi.html#using-the-command-line.
  - For the PS4 Controller to bo discoverable, hold the "share" and the "ps" button long enough for the controller to blink fast. 
- Can be used along a camera streaming software.
  - For example [silvanmelchior/RPi_Cam_Web_Interface](https://github.com/silvanmelchior/RPi_Cam_Web_Interface) which is a very good wrapper of motion and raspimjpeg.

# Hardware
- Raspberry Pi Zero W with a Sphero RVR.
- The Pi is powered via the RVR battery and connected to it via UART: see [this guide](https://sdk.sphero.com/raspberry-pi-setup/python-sdk-setup) for pinout.

This same guide contains a link to a Raspbian installation pre-configured with the SDK, which points here: https://drive.google.com/file/d/1V2xrvWRZFlGgbFs5HNWLvHeKjt7r4--u/view?usp=sharing.

TODO Add the startup script that launchs the Python Script, along with the start.sh of **Rpi Cam Web Interface**

Known issues: When using the joysticks to control the RVR instead of the directional arrows,
a race condition may occur randomly, inhibiting RVR control, in that case the controller is still responsive and the shutdown sequence (□□○○□○□○) works. 
