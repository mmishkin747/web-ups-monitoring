import socket
"""
socket.gethostname()
"""
# Connect to the server with `telnet $HOSTNAME 5000`.


def telnet_server_test():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('127.0.0.1', 2065))
    server.listen(5)

    connections = []

    while True:
        try:
            connection, address = server.accept()
            connection.setblocking(False)
            connections.append(connection)
        except BlockingIOError:
            pass

        for connection in connections:
            try:
                message = connection.recv(4096)
                
            except BlockingIOError:
                continue

            match message:
                case b'Y':
                    connection.send(b'')
                case b'C':
                    connection.send(b'21\r\n')
                case b'L':
                    connection.send(b'220\r\n')
                case b'f':
                    connection.send(b'100\r\n')
                case b'0':
                    connection.send(b'99\r\n')
                case b'j':
                    connection.send(b'60\r\n')
                case b'P':
                    connection.send(b'50\r\n')
                    server.close()                  
                    return print('------------Telnet server deaded-----------')

