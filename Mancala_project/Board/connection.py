"""
this file define the blueprint of Connection class where is handled connection between server and client
"""
import socket
import pickle


class Connection:
    def __init__(self):
        """Connection constructor where are initialized the socket, server address, port and which player is"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 2929
        self.addr = (self.server, self.port)
        self.player_id = self.connect()

    def get_player_id(self):
        """return which player client is"""
        return self.player_id

    def connect(self):
        """
        when is called, is making connection with server
        :return: what server send, which player is ( 0/1 )
        """
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(str(e))

    def send(self, data):
        """
        sending data from client to server and from server to client
        after data is send to server, we prepare for receiving bytes
        when this function is called is when client send the index from game's board he want to move
        and receive the object game updated to update the pygame window
        :param data: a string, what client send through socket
        :return: what server send, might be game object address
        """
        try:
            self.client.send(str.encode(data))  # sending data from client to server
            PAD_SIZE = 10
            full_message = b''
            new_data = True
            object_len = 0

            while True:  # I prepare to receive whole bytes from server because the data he send might be more
                # then 4096 bytes so i concatenate all to send all data
                info = self.client.recv(2048*2)

                if new_data:
                    # print("full message len", info[:PAD_SIZE])
                    object_len = int(info[:PAD_SIZE])  # first data received contain the length of full message
                    new_data = False
                full_message += info
                if len(full_message)-PAD_SIZE == object_len:  # when is received whole message, is send to client
                    # print("full msg received")
                    return pickle.loads(full_message[PAD_SIZE:])
        except socket.error as e:
            print(e)
