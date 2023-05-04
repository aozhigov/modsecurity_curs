import os
import sys

# Проверяем, что путь к папке был передан в аргументах
if len(sys.argv) != 3:
    sys.exit(1)

# Получаем путь к папке из аргументов
folder_path = sys.argv[1]
count_user = sys.argv[2]
host = sys.argv[3]
port = sys.argv[4]
login = sys.argv[5]
password = sys.argv[6]

# Проверяем, что директория существует
if not os.path.isdir(folder_path):
    print(f"Папка '{folder_path}' не существует")
    sys.exit(1)

# Получаем список файлов в папке
files = os.listdir(folder_path)

# Проходимся по списку файлов и запускаем каждый из них
for file in files:
    # Фильтруем файлы по расширению (можно изменить на своё)
    if file.endswith(".jmx"):
        # Формируем команду для запуска файла
        command = "/jmeter.sh -Jthreads=" + count_user + " -Jhost=" + host + " -Jport=" + port + " -Jlogin=" + login + " -Jpassword=" + password + " -n -t " + os.path.join(folder_path, file)
        # Запускаем файл в терминале
        os.system(command)
