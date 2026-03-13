import socket
import threading

HOST = "127.0.0.3"
PORT = 49271

def handle_client(conn, addr):
    """Функция для обработки подключения одного клиента"""
    print(f"Connected by {addr}")
    try:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"[{addr}] Received: {message}")
            
            # Проверяем, не хочет ли клиент выйти
            if message.lower().strip() == "/exit":
                print(f"Client {addr} requested to disconnect.")
                conn.sendall(b"Goodbye!")
                break  # Выходим из цикла, что приведет к закрытию соединения
            
            # Отправляем обратно (эхо)
            conn.sendall(data)
            
    except (ConnectionResetError, ConnectionAbortedError):
        print(f"Client {addr} disconnected abruptly.")
    except Exception as e:
        print(f"Error with client {addr}: {e}")
    finally:
        conn.close()
        print(f"Connection with {addr} closed.")

def start_server():
    """Функция запуска сервера"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Позволяет переиспользовать адрес
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    
    print(f"Server listening on {HOST}:{PORT}")
    print("Press Ctrl+C to stop the server")
    
    try:
        while True:
            # Принимаем новое подключение
            conn, addr = server_socket.accept()
            
            # Создаем новый поток для обработки клиента
            client_thread = threading.Thread(target=handle_client, args=(conn, addr))
            client_thread.daemon = True
            client_thread.start()
            
            print(f"Active connections: {threading.active_count() - 1}")
            
    except KeyboardInterrupt:
        print("\nServer shutting down...")
    except Exception as e:
        print(f"Server error: {e}")
    finally:
        server_socket.close()
        print("Server stopped.")

if __name__ == "__main__":
    start_server()
