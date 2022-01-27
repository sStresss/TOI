import constant
import socket


def sock_connect(buffer):
    sock = socket.socket()
    sock.connect((constant.hostIP, buffer))
    return sock


def send_board(command, sock, buffer):
    data_asc = command.encode()
    data_hex = data_asc.fromhex(command)
    sock.send(data_hex)
    resp = sock.recv(buffer)
    # print('SEND: ', data_asc)
    # print('RESPONCE: ', resp)

    return resp
