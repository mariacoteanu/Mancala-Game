"""
this file define the blueprint of Connection class where is handled connection between server and client
"""
import socket
import pickle


class Connection:
    def __init__(self):
        """Connection contructor where are initialized the socket, server address, port and which player is"""
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "127.0.0.1"
        self.port = 2929
        self.addr = (self.server, self.port)
        self.p = self.connect()

    def getP(self):
        """return which player client is"""
        return self.p

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
            PADSIZE = 10
            fullmessage = b''
            new_data = True
            objlen = 0
            while True:  # I prepare to receive whole bytes from server because the data he send might be more
                # then 4096 bytes so i concatenate all to send all data
                info = self.client.recv(2048 * 2)
                if new_data:
                    # print("full message len", info[:PADSIZE])
                    objlen = int(info[:PADSIZE])  # first data received contain the length of full message
                    new_data = False
                fullmessage += info
                if len(fullmessage) - PADSIZE == objlen:  # when is received whole message, is send to client
                    # print("full msg received")
                    return pickle.loads(fullmessage[PADSIZE:])
        except socket.error as e:
            print(e)
