from random import uniform
import socket
import time
"""
socket.gethostname()
"""

# Connect to the server with `telnet $HOSTNAME 5000`.
# 
def telnet_server_test(port:int=2065, main_voltage:int=220, no_valid:bool=False, no_value:bool=False):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('127.0.0.1', port))
    server.listen(5)

    connections = []
    serv_sleep = 0.0
    
    if no_valid:
        main_voltage = bytes('data' + '\n', encoding="utf-8")
    else:
        main_voltage = bytes(str(main_voltage) + "\n", encoding = "utf-8")

    if no_value:
        load = b''
        voltage = b''

    else:
        load = b'50\r\n'
        voltage = b'24'
        

    while True:

        try:
            connection, address = server.accept()
            connection.setblocking(True)
            connections.append(connection)
        except BlockingIOError:
            pass

        for connection in connections:
            try:
                
                message = connection.recv(4096)
                           
            except BlockingIOError:
                continue
            if not message:
                continue
            rand_num = uniform(0,3)
            time.sleep(rand_num)
            serv_sleep += rand_num
            
            match message:
                case b'Y':
                    connection.send(b'SM\r\n')
                case b'C':
                    connection.send(b'21\r\n')
                case b'L':
                    connection.send(main_voltage)
                case b'f':
                    connection.send(b'100\r\n')
                case b'0':
                    connection.send(b'99\r\n')
                case b'j':
                    connection.send(b'60\r\n')
                case b'P':
                    connection.send(load)   
                case b'\x01':
                    connection.send(b'ModelTest')
                case b'B':
                    connection.send(voltage)
                case b'W':
                    connection.send(b'Ok')
                case b'm':
                    connection.send(b'01/01/22')
                case b'x':
                    connection.send(b'01/02/22')
                case b'n':
                    connection.send(b'0000test0000')
                case b'close\r\n':
                    server.close()    
                    return 

if __name__=="__main__":
    telnet_server_test()

