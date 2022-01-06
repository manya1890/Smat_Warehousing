# Import QRCode from pyqrcode
import pyqrcode
import png
from pyqrcode import QRCode





def generateQrCode(product_details, product_name):
    # String which represents the QR code is product_details

    # Generate QR code
    url = pyqrcode.create(product_details)

    # Create and save the png file naming "myqr.png"
    url.png(f'Product\qrcode\{product_name}.png', scale = 6)


def scanBarcode():
    return 0 