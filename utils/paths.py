import os


def set_path(filename):
    return os.path.join(
        os.path.join(os.path.abspath('.'), 'reports_dir'),
        filename
    )
