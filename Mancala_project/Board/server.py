"""
in this file is the server logics, where connections are made and processing data
"""
import socket
from _thread import *
import pickle
from networkgame import NetworkGame

server = "127.0.0.1"
port = 2929

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print(str(e))

s.listen()
print("Am pornit serverul. Astept clienti ....")

connected = set()
games = {}
idPlayer = 0
PADSIZE = 10


def threaded_client(clientConn, player, game_id):
    # threaded function for every client, where is the sending and receiving data logic
    global idPlayer
    clientConn.send(str.encode(str(player)))  # first is sent to client which player is ( 0 / 1 )

    while True:
        try:
            data = clientConn.recv(4096).decode()  # receive what to send back to client
            if game_id in games:
                game = games[game_id]  # find the game object address specified for gameId
                if not data:
                    print("No data")
                    break
                else:
                    if data != "get":
                        game.move(int(data), player)  # based on the index chosen by client, is performed the move
                    reply = pickle.dumps(game)  # then the updated game object is send to both clients
                    # to update their window
                    reply = bytes(f"{len(reply):<{PADSIZE}}", 'utf-8') + reply  # modify the bytes so the length of data
                    # to be know for sending to client and waiting to receive all bytes
                    clientConn.sendall(reply)
            else:
                print("No gameId")
                break
        except Exception as ex:
            print("Error: " + str(ex))
            break

    print("Lost connection")
    try:
        print(f"player {player} close game....")
        del games[game_id]
        print("Closing Game", game_id)
    except Exception as ex:
        print("Can't delete game\n" + str(ex))
        pass
    idPlayer -= 1
    clientConn.close()  # close connection


if __name__ == "__main__":
    while True:
        conn, addr = s.accept()  # accept client connection
        print("Conectat:", addr)

        idPlayer += 1
        p = 0
        gameId = (idPlayer - 1) // 2
        if idPlayer % 2 == 1:
            games[gameId] = NetworkGame(gameId)  # when two clients are connected, start new Game
            print("----- Creez un nou joc -----")
        else:
            games[gameId].ready = True  # when only one is connected, wait for another partner
            p = 1

        start_new_thread(threaded_client, (conn, p, gameId))  # start new thread
