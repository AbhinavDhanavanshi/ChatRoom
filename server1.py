import threading
import os
import socket
import argparse

class Server(threading.Thread):
    
    def __init__(self, host, port):
        super().__init__()
        self.curr_connections = []
        threading.Thread.__init__(self)
        self.host = host
        self.port = port
    
    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        
        while True:
            client_socket, address = self.server_socket.accept()
            print(f"Accepted connection from {address}.")
            server_socket = ServerSocket(client_socket, address, self)
            server_socket.start()
            self.curr_connections.append((client_socket, address))
            
    def sendAll(self, message, address):
        for connection in self.curr_connections:
            print(f"there are {len(self.curr_connections)} connections")
            print(connection)
            if connection[1] != address:
                try:
                    connection[0].sendall(f"{message}".encode('ascii'))
                except:
                    print(f"{connection[1]} has left the chat.")
                
    def remove_connection(self, connection):
        self.curr_connections.remove(connection)
        
class ServerSocket(threading.Thread):
    def __init__(self, server_socket, address, server):
        super().__init__()
        self.server_socket=server_socket
        self.address=address
        self.server=server
        
    def run(self):
        while True:
            message = self.server_socket.recv(1024).decode('ascii')
            
            if message:
                print(f"{message}")
                self.server.sendAll(message, self.address)
                
            else:
                print(f"{self.address} left the chat.")
                self.server.remove_connection(self)
                self.server_socket.close()
                break
            
    def send(self,message):
        self.server_socket.sendall(message.encode('ascii'))       
        
    def exit_server(server):
        while True:
            status=input("")
            if status=="exit":
                print("terminating all connections")
                for connection in server.connections:
                    Server.remove_connection(connection)
                print("shutting down server")
                os.exit(0)
            
SERVER_HOST = '172.31.18.45'
SERVER_PORT = 12345

server=Server(SERVER_HOST, SERVER_PORT)
server.start_server()
exit=threading.Thread(target=ServerSocket.exit_server, args=(server,))
exit()

    