import cv2
import ast

from pyzbar.pyzbar import decode, ZBarSymbol
from PIL import Image

def read_qr():
    capture = cv2.VideoCapture(0)
    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        decoded = decode(image, symbols=[ZBarSymbol.QRCODE])

        if (len(decoded) > 0):
            decoded_data = ast.literal_eval(decoded[0].data)
            address = decoded_data.get("address")
            if (address != None):
                capture.release()
                return(address)

print(read_qr())
