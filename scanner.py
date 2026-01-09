import cv2
import time
from picamera2 import Picamera2
from pyzbar.pyzbar import decode

TMP_IMG = "/dev/shm/qrcap.jpg"

class QRScanner:
    def __init__(self):
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(
            main={"size": (1280, 720)},
            buffer_count=1
        )
        self.picam2.configure(config)
        self.picam2.start()

    def read(self):
        self.picam2.capture_file(TMP_IMG)
        img = cv2.imread(TMP_IMG)

        codes = decode(img)
        if not codes:
            return None

        return codes[0].data.decode("utf-8").strip()

    def stop(self):
        self.picam2.stop()
