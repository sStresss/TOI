import constant
import toi_connect


def temperature():
    sock = toi_connect.sock_connect(buffer=16603)
    buffer = 4096
    toi_connect.send_board(constant.login, sock, buffer)
    sock = toi_connect.sock_connect(buffer=5200)
    toi_connect.send_board(command, sock, buffer)
    resp = toi_connect.send_board(command, sock, buffer)
    resp = str(resp)
    a = resp.split(sep="previewValue", maxsplit=14)
    b = a[11][3:]
    bd = b.find('"')
    bb = b[:bd]
    print('Температура:', bb, 'гр. Цельсия')
    return bb


def main():
    print('311')
    #temperature()
    return '22'


if __name__ == "__main__":
    #test = sys.argv[1]
    #print(test)
    command = ''

    main()

