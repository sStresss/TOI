import constant
import toi_connect


def testing(command_test):
    sock = toi_connect.sock_connect(buffer=16603)
    buffer = 4096
    toi_connect.send_board(constant.login, sock, buffer)
    sock = toi_connect.sock_connect(buffer=5200)
    toi_connect.send_board(command_test, sock, buffer)


def main(com):
    a = toi_connect.sock_connect(buffer=16603)
    testing(com)
    print(a)


if __name__ == "__main__":
    # test = sys.argv[1]
    test = 'vertical'
    print(test)
    command = ''

    if test == 'on_display':
        print('in on display')
        command = '55aa00d9fe000100ffff0100000100020100003059'

    if test == 'off_display':
        print('in off display')
        command = '55aa003ffe000100ffff0100000100020100ff9559'

    if test == 'diagonal':
        print('in diagonal display')
        command = '55aa0025fe000100ffff0100010100020100088558'

    if test == 'vertical':
        print('in vertical display')
        command = '55aa0081fe000100ffff010001010002010007e058'
        # command = '55aa00d7fe000100ffff0100010100020100073659'

    if test == 'horizon':
        print('in horizon display')
        command = '55aa0035fe000100ffff0100010100020100069358'

    if test == 'back_display':
        print('in back display')
        command = '170303003000000000000001748723498376594d92a606468d6a5e74bf5f4879b1460563a2374c05561869ab3885596ee953a7bfb4'
        #command = '55aa008bfe000100ffff010001010002010001e458'

    main(command)

