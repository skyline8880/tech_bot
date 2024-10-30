import os

# Путь к текущей директории проекта
current_directory = os.getcwd()


def set_path(filename):
    return os.path.join(
        os.path.join(os.path.abspath('.'), 'reports_dir'),
        filename
    )
