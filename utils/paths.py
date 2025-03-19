import os
import sys


def set_path(filename):
    return os.path.join(
        os.path.join(os.path.abspath('.'), 'reports_dir'),
        filename
    )


def path_to_no_photo_pic():
    separator = "/"
    if sys.platform == 'win32':
        separator = "\\"
    return f"no_photo_dir{separator}no_photo.png"
