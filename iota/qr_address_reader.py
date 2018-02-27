import cv2
import ast

from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image

ADDRESS_IDENTIFIER = "address"

def read_qr(identifier):
    try:
        capture = cv2.VideoCapture(0)
        while True:
            ret, frame = capture.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            image = Image.fromarray(gray)
            decoded = decode(image, symbols=[ZBarSymbol.QRCODE])

            if (len(decoded) > 0):
                return ast.literal_eval(decoded[0].data).get(identifier)
    finally:
        capture.release()
