import json
from collections import Counter
import constant
import toi_connect


def create_dict_module():
    data_in = {}

    for cabinet in range(1, 13, 1):
        cabinet = str(cabinet)
        data_in[cabinet] = {}
        data_in[cabinet]['col'] = 1
        data_in[cabinet]['percent'] = 1
        for module in range(1, 26, 1):
            module = str(module)
            data_in[cabinet][module] = {}
            data_in[cabinet][module]['mod_col'] = 1
            data_in[cabinet][module]['r_col'] = 1
            data_in[cabinet][module]['g_col'] = 1
            data_in[cabinet][module]['b_col'] = 1
            data_in[cabinet][module]['red'] = ''
            data_in[cabinet][module]['green'] = ''
            data_in[cabinet][module]['blue'] = ''
    return data_in


def monitor(all_cab):

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

    def create_part_module_pix(test_hex_part):
        print('test_hex', len(test_hex_part))
        list_pair_hex = create_list_pair(test_hex_part)
        print('1', list_pair_hex)

        def sort_color_hex(step):
            down_list = []
            up_list = []
            count = 1
            for part in list_pair_hex[step:step + 160]:
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

        red_all = create_list_binary(red_up) + create_list_binary(red_down)
        green_all = create_list_binary(green_up) + create_list_binary(green_down)
        blue_all = create_list_binary(blue_up) + create_list_binary(blue_down)

        return red_all, green_all, blue_all

    def create_final_list(color_list):
        z_list = []
        for step_ik in range(10):
            red_5 = color_list[step_ik::5]
            z_list.append(red_5)
        return z_list
    # sock = toi_connect.sock_connect(buffer=16603)
    # buffer = 4096
    # toi_connect.send_board(constant.login, sock, buffer)
    # sock = toi_connect.sock_connect(buffer=5200)
    #
    # resp = toi_connect.send_board(command, sock, buffer)

    # a = bytearray(resp)
    # hex шестнадцатиричный формат
    # hex_all = a.hex()
    # # hex_part = hex_all[36:-68]
    # hex_part = hex_all[36:-132]
    # print('hex_part', hex_part)
    # print(len(hex_part))
    test_hex_part_1 = '00f7ffffffffffffffffffffffffffffdfffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffff7fffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7ffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffff7'
    test_hex_part_2 = '77ffffffffffffffffffffffffffffffdfffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffff7fffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff7ffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff' \
                      'fffffffffffffffffffffffffffff7'

    all_request_list = []
    for _ in range(10):
        n = 0
        list_1 = []
        for _ in part:
        if _ % 2 == 0:
            list_1.append(all_request_list[_: _ + 2])
            n += 1
        if
        all_request_list.append(test_hex_part_1)

    red_1, green_1, blue_1 = create_part_module_pix(test_hex_part_1)
    red_2, green_2, blue_2 = create_part_module_pix(test_hex_part_2)
    red = red_1 + red_2
    green = green_1 + green_2
    blue = blue_1 + blue_2

    list_red = create_final_list(red)
    list_green = create_final_list(green)
    list_blue = create_final_list(blue)

    for cabinet in all_cab:
        if cabinet == '1':
            for item_ in all_cab[cabinet]:
                if 'col' in item_:
                    continue
                if 'percent' in item_:
                    continue
                else:
                    for module in all_cab[cabinet][item_]:
                        if 'red' in module and int(item_) <= 5:
                            all_cab[cabinet][item_][module] = list_red[int(item_) - 1]
                        if 'green' in module and int(item_) <= 5:
                            all_cab[cabinet][item_][module] = list_green[int(item_) - 1]
                        if 'blue' in module and int(item_) <= 5:
                            all_cab[cabinet][item_][module] = list_blue[int(item_) - 1]
    return all_cab


def calculate_broke_pixel_and_sen_json(all_data):
    for item in all_data:
        list_module_broke_pixel_count = []

        for cabinet in all_data[item]:
            if 'col' in cabinet:
                continue
            if 'percent' in cabinet:
                continue
            else:
                broke_pixel = 0

                for module in all_data[item][cabinet]:
                    broke_red = 0
                    broke_green = 0
                    broke_blue = 0
                    if 'mod_col' in module:
                        continue
                    if 'r_col' in module:
                        continue
                    if 'g_col' in module:
                        continue
                    if 'b_col' in module:
                        continue
                    for broke_pix in all_data[item][cabinet][module]:
                        count_pix_0 = Counter(broke_pix)['0']
                        broke_pixel += count_pix_0
                    print('zzzz', all_data[item][cabinet]['red'])
                    for rr in all_data[item][cabinet]['red']:
                        broke_red += Counter(rr)['0']
                    for gg in all_data[item][cabinet]['green']:
                        broke_green += Counter(gg)['0']
                    for bb in all_data[item][cabinet]['blue']:
                        broke_blue += Counter(bb)['0']
                    all_data[item][cabinet]['r_col'] = broke_red
                    all_data[item][cabinet]['g_col'] = broke_green
                    all_data[item][cabinet]['b_col'] = broke_blue

                list_module_broke_pixel_count.append(broke_pixel)
                all_data[item][cabinet]['mod_col'] = broke_pixel

        cabinet_count = sum(list_module_broke_pixel_count)
        percent_broken_pixel = cabinet_count * 100 / 38400
        percent_broken_pixel = round(percent_broken_pixel, 3)

        all_data[item]['col'] = cabinet_count
        all_data[item]['percent'] = percent_broken_pixel

    with open("../static/timetable/monitor2.json", "w") as write_file:
        json.dump(all_data, write_file, indent=4)


def main():
    data = create_dict_module()
    all_cabinets = monitor(data)
    calculate_broke_pixel_and_sen_json(all_cabinets)
    # monitor()


if __name__ == "__main__":
    main()
