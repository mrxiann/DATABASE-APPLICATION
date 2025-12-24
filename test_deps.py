import mysql.connector
import qrcode
from PIL import Image

print("✅ MySQL Connector version:", mysql.connector.__version__)
print("✅ QRCode installed successfully")
print("✅ Pillow (PIL) version:", Image.__version__)

# Test QR code generation
qr = qrcode.QRCode(version=1, box_size=10, border=4)
qr.add_data("Test")
qr.make(fit=True)
print("✅ QR code generation works!")