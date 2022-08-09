from random import uniform
import socket
import time
"""
socket.gethostname()
"""

# Connect to the server with `telnet $HOSTNAME 5000`.
# 
#shoud add param badparam and goodparam
def telnet_server_test(main_voltage:int=220, no_valid:bool=False):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setblocking(False)
    server.bind(('127.0.0.1', 2065))
    server.listen(5)

    connections = []
    telnet_close = False
    serv_sleep = 0.0
    
    if no_valid:
        main_voltage = bytes('data' + '\n', encoding="utf-8")
    else:
        
        main_voltage = bytes(str(main_voltage) + "\n", encoding = "utf-8")

    while True:
        if telnet_close == True:
            
            return print('------------Telnet server deaded-----------')
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
            print(message)
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
                    connection.send(b'50\r\n')   
                    print(f'------------Server sleped at {serv_sleep} ')
                    #telnet_close = True
                case b'close\r\n':
                    return

if __name__=="__main__":
    telnet_server_test()

