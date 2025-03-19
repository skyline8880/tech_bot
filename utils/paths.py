import os
import sys

from PIL import Image, ImageDraw, ImageFont


def set_path(filename):
    return os.path.join(
        os.path.join(os.path.abspath('.'), 'reports_dir'),
        filename
    )


def create_no_photo_pic():
    img = Image.new('RGB', (500, 500), color="white")
    font = ImageFont.load_default(size=25)
    if sys.platform == 'win32':
        font = ImageFont.truetype(
            font="arial.ttf", size=25, encoding="UTF-8")
    d = ImageDraw.Draw(img)
    d.multiline_text(
        xy=(130, 200),
        text="Фото заявки удалено\n с сервера телеграм",
        fill="black",
        font=font)
    no_photo = "no_photo.png"
    img.save(no_photo)
    return no_photo
