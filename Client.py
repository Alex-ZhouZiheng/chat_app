import socket
import threading


HOST = 'localhost'
PORT = 2345
ADDR = (HOST, PORT)


class Client:
    def __init__(self, name):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.running = False  # Control flag for threads
        self.name = name
        self.thread = None
        self.messages = []

    # Connect to the server
    def start(self):
        self.client.connect(ADDR)
        self.running = True

        # Start the thread to receive messages
        self.thread = threading.Thread(target=self.receive)
        self.thread.daemon = True  # Ensure the thread stops with the program
        self.thread.start()

        # Send the username to the server
        self.client.send(self.name.encode('utf-8'))


    def receive(self):
        while self.running:
            try:
                # Receive messages from the server
                data = self.client.recv(1024).decode('utf-8')
                if not data:  # If no data, the server likely closed the connection
                    break

                if data.startswith("USER_LIST:"):
                    users = data[len("USER_LIST:"):].split(',')
                    self.messages.append(("USER_LIST", users))

                if data.startswith("MESSAGE:"):
                    message = data[len("MESSAGE:"):]
                    self.messages.append(("MESSAGE", message))

            except Exception as e:
                if self.running:  # Only print errors if still running
                    print(f"Error receiving data: {e}")
                break

    def send_message(self, message):
        self.client.send(message.encode('utf-8'))

    def get_message(self):
        new_messages = self.messages.copy()
        self.messages.clear()
        return new_messages

    def close(self):
        # Gracefully shut down the client
        self.running = False  # Stop the thread loop
        try:
            self.client.close()
        except Exception as e:
            print(f"Error closing client socket: {e}")
        print("Disconnected from server.")


