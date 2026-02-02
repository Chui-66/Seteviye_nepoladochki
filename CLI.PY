import socket  # Импорт модуля для работы с сетевыми соединениями

HOST = "10.90.14.78"  # IP-адрес сервера для подключения
PORT = 13337  # Номер порта сервера

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:  # Создание TCP-сокета
    s.connect((HOST, PORT))  # Подключение к серверу по указанному адресу и порту
    s.sendall(b"Hello, world")  # Отправка байтовой строки серверу
    data = s.recv(1024)  # Получение ответа от сервера (максимум 1024 байта)

print(f"Received {data!r}")  # Вывод полученных данных