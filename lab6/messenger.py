import socket

HOST = "127.0.0.1"
PORT_OBJECT2 = 50102
PORT_OBJECT3 = 50103

def send_message(port, text, timeout=3.0):
    try:
        with socket.create_connection((HOST, port), timeout=timeout) as conn:
            conn.sendall(text.encode("utf-8"))
            conn.shutdown(socket.SHUT_WR) 

            reply = b""
            while True:
                chunk = conn.recv(4096)
                if not chunk:  
                    break
                reply += chunk
            return reply.decode("utf-8")
    except OSError:
        return None

def open_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((HOST, port))
    except OSError:
        server.close()
        return None
    server.listen(5)
    server.setblocking(False)
    return server

def handle_one_request(server, handler):
    try:
        conn, _ = server.accept()
    except BlockingIOError:
        return

    with conn:
        conn.settimeout(2.0)
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk

        reply = handler(data.decode("utf-8"))
        conn.sendall(reply.encode("utf-8"))