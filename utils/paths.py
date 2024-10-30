import os

# Путь к текущей директории проекта
current_directory = os.getcwd()

# Имя папки, которую нужно создать
# folder_name = "reports_dir"

# Полный путь к папке "reports_dir"
# reports_dir = os.path.join(current_directory, folder_name)

# Создание папки "reports_dir" (если она не существует)
# if not os.path.exists(reports_dir):
    # os.makedirs(reports_dir)

# print(f'Папка "{folder_name}" успешно создана в директории проекта.')


def set_path(filename):
    return os.path.join(
        os.path.join(os.path.abspath('.'), 'reports_dir'),
        filename
    )
