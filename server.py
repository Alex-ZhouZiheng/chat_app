import socket
import threading

SERVER = 'localhost'
PORT = 2345
ADDR = (SERVER, PORT)


class Server:
    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(ADDR)
        self.server.listen()
        self.clients = {}

# Handle client connection,receive message from client and broadcast to all clients
    def handle_client(self,conn):
        try:
            name = conn.recv(1024).decode('utf-8')
            print(f"[NEW CONNECTION] {name} Aconnected.")
            self.clients[conn] = name
            self.broadcast_user_list()

            while True:
                data = conn.recv(1024).decode('utf-8')
                if not data:
                    print(f"[{name}] has disconnected.")
                    self.broadcast_user_list()
                    break
                print(f"[{name}] {data}")
                self.broadcast(f"{name}:{data}", conn)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            conn.close()
            self.clients.pop(conn,None)
            self.broadcast_user_list()
            #self.broadcast(f"{name} has left the chat.", conn)


    # Broadcast message to all clients
    def broadcast(self,message, sender_conn):
        for cl in self.clients.keys():
            if cl != sender_conn:  # don't send the message to the sender
                try:
                    cl.send(f"MESSAGE:{message}".encode('utf-8'))
                except Exception as e:
                    print(f"Error sending message to client: {e}")


    def broadcast_user_list(self):
        user_list = list(self.clients.values())
        message = f"USER_LIST:{','.join(user_list)}"  # Format the user list as a special message
        for cl in self.clients.keys():
            try:
                cl.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Error sending user list to client: {e}")


    # Start the server
    def start_server(self):
        while True:
            conn, addr = self.server.accept()
            thread = threading.Thread(target=self.handle_client, args=(conn,))
            thread.start()
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")  # -1 because the main thread is also counted


if __name__ == '__main__':
    server = Server()
    Server.start_server(server)
