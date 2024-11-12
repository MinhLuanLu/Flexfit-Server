import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def Generate_QRCode(namefile, message):
    img = qrcode.make(message)  # Or whatever data you want
    img_io = BytesIO()
    img.save(img_io, format='PNG')
    img_io.seek(0)
    return ContentFile(img_io.getvalue(), name=f'{namefile}.png')  # Save and Return as ContentFile
