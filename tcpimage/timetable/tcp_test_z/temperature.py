import constant
import toi_connect

def monitor():
    # command = '55aa00e9fe000100ffff0100170000010100005559' # мигает при начале сканирования
    # command = '55aa006afe000100000000000000000b0001ca56'  # working 1
    command = '55aa0089fe000100000000000000000b0001e956'  # activate monitoring

    def hex_to_binary(hex_1):
        return return_binary_str(int(hex_1, 16))

    def return_binary_str(num):
        binary_str = ''
        if num < 0:
            pass
        if num == 0:
            return '00000000'
        while num > 0:
            binary_str = str(num % 2) + binary_str
            num = num >> 1
        if len(binary_str) < 8:
            k = 8 - len(binary_str)
            binary_str = '0' * k + binary_str
        return binary_str

    def create_list_pair(part):
        n = 0
        list_1 = []
        for _ in part:
            if n % 2 == 0:
                list_1.append(part[n: n + 2])
            n += 1
        return list_1

    sock = toi_connect.sock_connect(buffer=16603)
    buffer = 4096
    toi_connect.send_board(constant.login, sock, buffer)
    sock = toi_connect.sock_connect(buffer=5200)

    resp = toi_connect.send_board(command, sock, buffer)

    a = bytearray(resp)
    # hex шестнадцатиричный формат
    hex_all = a.hex()
    # hex_part = hex_all[36:-68]
    hex_part = hex_all[36:-132]
    print('hex_part', hex_part)
    print(len(hex_part))
    test_hex_part = 'f7fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7'
    print('test_hex', len(test_hex_part))
    list_pair_hex = create_list_pair(test_hex_part)
    print('1', list_pair_hex)

    def sort_color_hex(step):
        down_list = []
        up_list = []
        count = 1
        for part in list_pair_hex[step:step+160]:
        # for part in list_pair_hex[step:step+64]:
            if count % 2 == 0:
                down_list.append(part)
            else:
                up_list.append(part)
            count += 1
        return up_list, down_list

    red_up, red_down = sort_color_hex(0)
    print('red_____up', red_up, len(red_up))
    print('red___down', red_down)
    # green_up, green_down = sort_color_hex(64)
    green_up, green_down = sort_color_hex(160)
    print('green___up', green_up)
    print('green_down', green_down)
    # blue_up, blue_down = sort_color_hex(128)
    blue_up, blue_down = sort_color_hex(320)
    print('blue____up', blue_up)
    print('blue__down', blue_down)

    def create_list_binary(list_hex):
        list_binary = []
        list_done = []
        num_ = 0
        for pix in list_hex:
            bin_pix = hex_to_binary(pix)
            if num_ < 16:
                list_binary.append(bin_pix)
            else:
                list_binary.append(bin_pix[::-1])
            num_ += 1
        for step in range(0, 80, 4):
            str_uniq = ''.join(list_binary[step:step + 4])
            list_done.append(str_uniq)
        return list_done
    red = create_list_binary(red_up) + create_list_binary(red_down)
    green = create_list_binary(green_up) + create_list_binary(green_down)
    blue = create_list_binary(blue_up) + create_list_binary(blue_down)
    print('red__', red, len(red))
    print('green', green)
    print('blue_', blue)


if __name__ == "__main__":
    monitor()
