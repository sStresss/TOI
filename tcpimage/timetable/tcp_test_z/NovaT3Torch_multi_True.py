import binascii
import itertools
import pprint
import socket
import os
import sys
import time
import hashlib
import shutil
import threading
import constant
import logging
from collections import Counter
from time import sleep
from termcolor import cprint
from random import randint
from openpyxl import load_workbook
import test


class UpdateBright:
    def __init__(self, input_bright, source_path):
        self.input_bright = input_bright
        self.source_path = source_path

    def set_bright(self):
        """Вызывается если change_brightness == True"""
        logging.debug(f"    Input bright: {self.input_bright}")
        sock = sock_connect(port=16603)
        port = 4096
        send_board(constant.login, sock, port)

        if len(self.input_bright) == 1:
            self.input_bright = '0' + self.input_bright
        if self.input_bright != '100':
            data_0 = 'AVON%\x00\x00\x00QR\x18\x00\x04\x01\x00\x00\x0e\x00\x00\x00\x00\x00\'\x02{"ratio":' \
                     + self.input_bright + '.0}'
        else:
            data_0 = 'AVON\x16\x00\x00\x00QR\x18\x00\x04\x01\x00\x00\x0f\x00\x00\x00\x00\x00\x19\x02{"ratio":100.0}'
        data_0 = data_0.encode()
        sock.send(data_0)
        sock.recv(4096)
        sock.close()


class AutoBright:
    def __init__(self, auto_bright_array, check_unicode, default_byte_block):
        self.auto_bright_array = auto_bright_array
        self.check_unicode = check_unicode
        self.default_byte_block = default_byte_block  # Байтовые строки в константте
        self.start_delta = 0
        self.time_data = ''

    def set_auto_bright(self):
        cprint('старт изменения авто-яркости', 'yellow')
        len_arr = len(self.auto_bright_array)
        sock = sock_connect(port=16603)
        port = 4096
        send_board(constant.login, sock, port)
        # считаем дельту смещения
        self.start_delta = self.find_delta()  # return 1
        count = 1
        start_block = ''

        for elem in self.default_byte_block:
            if count == len_arr:
                """реплеймим первый байт. если байт не чистый байт а с символом в конце, то просто инкрементируем символ 
                по ascii"""
                if len_arr == 3 or len_arr == 6 or len_arr == 9:
                    x = bytearray(elem[0], 'utf-8')
                    tmp_block = self.up_byte_time(elem=elem[1], x=x)
                    # реплейсим второй байт
                    curr_start_block = self.up_byte_time(elem=elem[2], x=tmp_block)
                    self.check_unicode = False
                    start_block = curr_start_block.decode('utf8')

                # если чистый байт, то смещаем сам байт
                else:
                    byte_elem = bytearray(elem[0], 'utf-8')
                    temps_block = self.up_byte(elem=elem[1], x=byte_elem)
                    start_block = self.up_byte(elem=elem[2], x=temps_block)
                    self.check_unicode = True
            count += 1

        data_main_block = ''

        inst = 1
        for elem in self.auto_bright_array:
            tmp_data_main_block = '{"type":1,"cron":["' + \
                                  str(elem[1]) + ' * * ? *"],"startTime":"2020-08-05 00:00:00","endTime":"4016-06-06 ' \
                                                 '23:59:59","args":[' + \
                                  str(elem[2]) + '.0],"segments":null,"opticalFailureInfo":null,"enable":' + \
                                  str(elem[0]) + '}'
            if inst == 1:
                data_main_block = data_main_block + tmp_data_main_block
            if inst > 1:
                data_main_block = data_main_block + ',' + tmp_data_main_block
            inst += 1
        data_end = '],"segmentConfig":{"args":[65534.0,0.0,100.0,0.0,1.0],"segments":[{"environmentBrightness":0.0,' \
                   '"screenBrightness":100.0}],"opticalFailureInfo":{"enable":true,"screenBrightness":10.0}},' \
                   '"timeStamp":"2020-08-05 00:36:34"}'
        if not self.check_unicode:
            data_start = start_block + '{"type":"BRIGHTNESS","source":{"type":1,"platform":2},"enable":true,' \
                                       '"conditions":['
            data_1 = bytearray(data_start + data_main_block + data_end, 'utf-8')
        else:
            data_start = start_block + b'{"type":"BRIGHTNESS","source":{"type":1,"platform":2},"enable":true,"conditions":['
            data_1 = data_start + bytearray(data_main_block + data_end, 'latin1')

        sock.send(data_1)
        bright_resp = str(sock.recv(512))  # Добавить в лог
        if len(bright_resp) < 4 or 'password' in bright_resp:
            raise Exception("    bad answer")
        cprint('    Ответ от платы: ' + bright_resp, 'green')
        sock.close()
        cprint('авто-яркость успешно изменена', 'yellow')

    def find_delta(self):
        start_delta = 0
        for elem in self.auto_bright_array:
            delta = 0
            self.time_data = elem[1]
            sec, min_, hour = self.find_sec_min_hour()

            if len(sec) > 1:
                delta += 1
            if len(min_) > 1:
                delta += 1
            if len(hour) > 1:
                delta += 1

            if len(elem[2]) > 1:
                delta += len(elem[2]) - 1
            start_delta += delta
        return start_delta

    def find_sec_min_hour(self):
        time_ = str(self.time_data).split(sep=" ", maxsplit=2)
        return time_[0], time_[1], time_[2]

    def up_byte_time(self, elem, x):
        byte_len_0 = len(elem)
        last_byte = elem[byte_len_0 - 1]
        last_byte_ascii = ord(last_byte) + self.start_delta
        up_last_byte = chr(last_byte_ascii)
        curr_elem = elem.replace(last_byte, up_last_byte)
        result = x.replace(bytearray(elem, 'utf-8'), bytearray(curr_elem, 'utf-8'))
        return result

    def up_byte(self, elem, x):
        elem_bytes = bytes(elem, 'latin1')
        curr_elem_utf8_num = ord(elem_bytes) + self.start_delta
        curr_elem = chr(curr_elem_utf8_num)
        result = x.replace(bytearray(elem, 'utf-8'), bytearray(curr_elem, 'latin1'))
        return result


def get_current_bright_mode():
    logging.debug('start get_current_bright in CurrentBright')
    sock = sock_connect(16606)
    port = 4096
    login = '160303004610000042410422cf31cbb0d7e60334b2e9d1c7ef7f17b424d48395d4f4e8d89d902528c88d5b2850f3143d9620a237990a8b0db73022e6832e37dd2c31626728e7d2a13a959214030300010116030300280000000000000000f8e7f371a7dbf1f9d79a2f77aaf0f86b780eb7d507a9409743a146baf371373b'
    a = send_board(login, sock, port)
    print('+++++++++++++++++++++++', a)
    # получаем ответ от платы по яркости
    mode = current_mode_bright(sock)
    if mode:
        current_bright_value_auto(sock)
        return True
    if not mode:
        # current_bright_value_manual()
        return False


def current_mode_bright(sock):
    # Получаем ответ по режиму яркости на плате auto|manual
    cprint('  Получаем ответ по режиму яркости на плате auto|manual', 'blue')
    port = 4096
    resp = send_board(constant.mode, sock, port)
    resp = str(resp)
    resp_split = resp.split(":", 1)
    resp_ = resp_split[1][:5]
    if 'true' in resp_:
        cprint('    Текущий режим работы яркости: автоматический', 'grey')
        return True
    elif 'BRIG' in resp_:
        cprint('    Текущий режим работы яркости: автоматический', 'grey')
        return True
    elif 'false' in resp_:
        cprint('    Текущий режим работы яркости: ручной', 'grey')
        return False
    else:
        'something wrong'


def current_bright_value_manual():
    sock = sock_connect(16603)
    port = 4096
    send_board(constant.login, sock, port)
    send_board(constant.check_manual_bright1, sock, port)
    resp = send_board(constant.check_manual_bright, sock, port)
    str_resp_z1 = str(resp)
    x = str_resp_z1.split(":", 1)
    x_1 = x[1]
    bright_man = x_1[:x_1.find(".")]
    print('bright current_bright_value_manual: ', bright_man)
    return bright_man


def current_bright_value_auto(sock):
    port = 4096
    resp = send_board(constant.bright_auto_mode, sock, port)
    resp = str(resp)
    resp_ = send_board(constant.check_manual_bright, sock, port)
    ls1 = str(resp_).find(":")
    cprint('    текущая яркость на плате в авто-режиме: ' + str(resp_)[ls1 + 1:ls1 + 3], 'magenta')
    z1_test = str(resp_)[ls1 + 1:ls1 + 3]
    print('22', z1_test)
    init_array = Counter(resp)
    count = init_array['?']
    for j in range(3):
        tmp_str = ''
        start_ind = resp.find("{")
        for _ in range(len(resp)):
            if _ > start_ind:
                tmp_str = tmp_str + resp[_]
        resp = tmp_str
    list_auto = []

    if resp.find("BRIGHTNESS") == -1:
        resp = resp.split(sep="cron", maxsplit=count)
        for k in resp:
            list_i = []
            if len(k) > 20:
                list_i.append(k[k.find('enable') + 8:k.find('}')])
                list_i.append(k[k.find('[') + 2:k.find('*') - 1])
                list_i.append(k[k.find("args") + 7:k.find(".")])
                list_auto.append(list_i)
    else:
        resp = resp.split(sep="enable", maxsplit=count)

        for n in resp:
            list_i = []
            if len(n) > 20:
                list_i.append(n[n.find(':') + 1:n.find(',')])
                list_i.append(n[n.find('[') + 2:n.find('*') - 1])
                list_i.append(n[n.find("args") + 7:n.find(".")])
                list_auto.append(list_i)

    cprint('    текущие значения на плате в авто-режиме: ' + str(list_auto), 'magenta')


class UpdateImage:
    def __init__(self, img_name, source_path, in_path, out_path):
        logging.debug('className: UpdateImage')
        self.img_name = img_name
        self.source_path = source_path
        self.in_path = in_path
        self.out_path = out_path
        self.data_list = constant.list_plat

    def run(self):
        logging.debug('    run')
        # print('    start run update image')
        """
        - формируем ресурсы проекта из входной картинки, картинку получаем из папки input, указатель имени картинки 
        получаем на вход модуля через api которого еще нет, пока определяем данное значение прямо в глобальных 
        переменных
        - сформированные ресурсы сохраняем в папку output для последующей отправки
        - считаем хеш md5 изображения 
        """

        print(self.img_name)
        #in_image = self.source_path + '/multi_input/' + self.img_name
        in_image = 'C:/TOI_prod/tcpimage/timetable/tcp_test_z/source/multi_input/' + self.img_name
        pic = open(in_image, 'rb')
        #pic_size = os.path.getsize(self.source_path + '/multi_input/' + self.img_name)
        pic_size = os.path.getsize('C:/TOI_prod/tcpimage/timetable/tcp_test_z/source/multi_input/' + self.img_name)

        logging.debug(f"      input image: {in_image}")
        logging.debug(f"      size input image: {pic_size}")

        data = pic.read()
        tmp_md5 = hashlib.md5(data)
        md5 = tmp_md5.hexdigest()
        pic.close()

        # копируем картинку с родным именем
        shutil.copyfile(self.in_path, self.out_path)

        # копируем картинку с md5 именем
        md5output_path = self.source_path + '/output/' + str(md5) + '.png'
        shutil.copyfile(self.in_path, md5output_path)

        sock = sock_connect(port=16602)

        # Отправляем файлы из папки output на плату
        self.sending_to_plata(sock)
        time.sleep(0.1)

        # отправляем картинку в каталог проекта
        self.sending_image_from_project_catalog(sock, md5)

        # отправляем картинку в каталог медиа
        self.sending_image_from_media_catalog(md5, sock)

        sock = sock_connect(port=16606)
        port = 4096
        # send_board(constant.run_proj1, sock, port)

        port = 1024

        # send_board(constant.login_tls1, sock, port)
        # send_board(constant.login_tls2, sock, port)
        # send_board(constant.login_tls3, sock, port)
        # send_board(constant.login_tls4, sock, port)
        # send_board(constant.login_tls5, sock, port)
        # send_board(constant.login_tls6, sock, port)

        # send_board(constant.run_proj2, sock, port)
        # logging.debug('        update 1 done!')
        #
        # send_board(constant.update2, sock, port)
        # logging.debug('        update 2 done!')

    def thread_img_load(self, data_port):
        logging.debug('            thread_img_load')
        # print('            start thread_img_load')
        # th = threading.Thread(target=self.img_load(data_port))
        # th.start()
        self.img_load(data_port)

    def img_load(self, data_port):
        logging.debug('            img_load')
        # print('                start img_load in ')
        sock = sock_connect(port=data_port)
        f = open(self.source_path + '/output/' + self.img_name, 'rb')
        while True:
            line = f.readline(512)
            if not line:
                break
            sock.send(line)
        sock.close()

    def sending_image_from_media_catalog(self, md5, sock):
        logging.debug('        sending_image_from_media_catalog')
        # print('        start sending_image_from_media_catalog')
        data = "PASV\n".encode()
        sock.sendall(data)
        resp_port = sock.recv(128)
        data = "STOR sdcard/nova/viplex_terminal/media/" + md5 + ".png\n"
        data = data.encode()
        sock.sendall(data)
        sock.recv(128)
        ftp_data_port = self.find_port_value(str(resp_port))
        self.thread_img_load(ftp_data_port)
        sock.close()

    def sending_image_from_project_catalog(self, sock, md5):
        logging.debug('        sending_image_from_project_catalog')
        # print('        start sending_image_from_project_catalog')
        data = "PASV\n".encode()
        sock.sendall(data)
        recv = sock.recv(128)
        resp_port = sock.recv(128)
        data = "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-24/1/" + md5 + ".png\n"
        data = data.encode()
        sock.sendall(data)
        sock.recv(128)
        ftp_data_port = self.find_port_value(str(resp_port))
        self.thread_img_load(ftp_data_port)
        sock.recv(1024)




    def sending_to_plata(self, sock):
        logging.debug('        sending_to_plat')
        resp1 = 0
        print('====TRY LOGIN====')
        i = 0
        resp1 = sock.recv(1024)
        for i in range(7):
            print('send: ', str(self.data_list[i]))
            data = self.data_list[i].encode()
            sock.sendall(data)
            resp1 = sock.recv(1024)
            print('resv: ', resp1)
        print('====LOGINED====')
        ftp_data_port = self.find_port_value(str(resp1))

        data = "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-24/1/planlist.json\n".encode()
        sock.sendall(data)
        resp1 = sock.recv(1024)

        data_sock = socket.socket()
        data_sock.connect((constant.hostIP, ftp_data_port))
        output_plan_list = os.path.join(self.source_path, '/output/planlist.json')
        f = open(output_plan_list, 'rb')
        file_size = os.path.getsize(output_plan_list)
        data = f.read(file_size)
        print('JSON PLANLIST SENDING TO DATAPORT: ', str(ftp_data_port))
        data_sock.sendall(data)
        # resp = sock.recv(1024)
        print('JSON PLANLIST SEND DONE')
        data_sock.close()
        time.sleep(0.1)

        data = "PASV\n".encode()
        sock.sendall(data)

        resp1 = sock.recv(1024)
        resp1 = sock.recv(1024)
        print('second data resv: ', resp1)
        ftp_data_port = self.find_port_value(str(resp1))

        data = "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-24/1/playlist0.json\n".encode()
        sock.sendall(data)
        resp1 = sock.recv(1024)

        data_sock = socket.socket()
        data_sock.connect((constant.hostIP, ftp_data_port))
        output_plan_list = os.path.join(self.source_path, '/output/playlist0.json')
        f = open(output_plan_list, 'rb')
        file_size = os.path.getsize(output_plan_list)
        data = f.read(file_size)
        print('JSON PLAYLIST SENDING TO DATAPORT: ', str(ftp_data_port))
        data_sock.sendall(data)
        # resp = sock.recv(1024)
        print('JSON PLAYLIST SEND DONE')
        data_sock.close()



    def find_port_value(self, value):
        logging.debug('            find_port_value')
        value_split = value.split(sep=",", maxsplit=5)
        value_split_2 = str(value_split[5]).find(")")
        port_num = int(value_split[4]) * 256 + int(value_split[5][0:value_split_2])
        return port_num


def sock_connect(port):
    sock = socket.socket()
    sock.connect((constant.hostIP, port))
    return sock


def clear_output_catalog(path):
    logging.debug('     clear_output_catalog')
    # print('        start clear_output_catalog')
    folder_path = os.path.join(path, 'output')
    for file_object in os.listdir(folder_path):
        file_object_path = os.path.join(folder_path, file_object)
        if os.path.isfile(file_object_path):
            os.unlink(file_object_path)
        else:
            shutil.rmtree(file_object_path)


def create_json_plan_list(md5, pic_size, source_path, raster_name):
    logging.debug('        create json plan_list and json plan_list0')

    print('        start create_json_plan_list')
    json_plan_list = 0
    json_playlist0 = 0
    if len(md5) == 1:
        json_plan_list = open(source_path + '/planlist1.json', 'r')
        json_playlist0 = open(source_path + '/playlist0_1.json', 'r')
    if len(md5) == 2:
        json_plan_list = open(source_path + 'planlist2.json', 'r')
        json_playlist0 = open(source_path + 'playlist0_2.json', 'r')
    if len(md5) == 3:
        json_plan_list = open(source_path + 'planlist3.json', 'r')
        json_playlist0 = open(source_path + 'playlist0_3.json', 'r')

    json_out_planlist = open(source_path + '/output/planlist.json', "a", encoding='utf8')
    ind = 1

    for line in json_plan_list:
        if ind == 34:
            line = '      \"fileName\": \"' + str(md5[0]) + '.png\",\n'
        if ind == 35:
            line = '      \"md5\": \"' + str(md5[0]) + '\",\n'
        if ind == 37:
            line = '      "size": ' + str(pic_size[0]) + '\n'

        if len(md5) == 2 or len(md5) == 3:
            if ind == 40:
                line = '      \"fileName\": \"' + str(md5[1]) + '.png\",\n'
            if ind == 41:
                line = '      \"md5\": \"' + str(md5[1]) + '\",\n'
            if ind == 43:
                line = '      "size": ' + str(pic_size[1]) + '\n'
        if len(md5) == 3:
            if ind == 46:
                line = '      \"fileName\": \"' + str(md5[2]) + '.png\",\n'
            if ind == 47:
                line = '      \"md5\": \"' + str(md5[2]) + '\",\n'
            if ind == 49:
                line = '      "size": ' + str(pic_size[2]) + '\n'

        json_out_planlist.write(line)
        ind += 1
    json_plan_list.close()
    json_out_planlist.close()

    json_out_playlist0 = open(source_path + '/output/playlist0.json', "a", encoding='utf8')

    ind_2 = 1

    for line in json_playlist0:
        if ind_2 == 94:
            line = "                  \"filesize\": " + str(pic_size[0]) + ",\n"
        if ind_2 == 97:
            line = "                  \"dataSource\": \"" + str(md5[0]) + ".png\",\n"
        if ind_2 == 101:
            line = "                  \"name\": \"" + str(raster_name[0]) + "\",\n"

        if len(md5) == 2:
            if ind_2 == 233:
                line = "                  \"filesize\": " + str(pic_size[1]) + ",\n"
            if ind_2 == 236:
                line = "                  \"dataSource\": \"" + str(md5[1]) + ".png\",\n"
            if ind_2 == 240:
                line = "                  \"name\": \"" + str(raster_name[1]) + "\",\n"

        if len(md5) == 3:
            if ind_2 == 232:
                line = "                  \"filesize\": " + str(pic_size[1]) + ",\n"
            if ind_2 == 235:
                line = "                  \"dataSource\": \"" + str(md5[1]) + ".png\",\n"
            if ind_2 == 239:
                line = "                  \"name\": \"" + str(raster_name[1]) + "\",\n"

            if ind_2 == 371:
                line = "                  \"filesize\": " + str(pic_size[2]) + ",\n"
            if ind_2 == 374:
                line = "                  \"dataSource\": \"" + str(md5[2]) + ".png\",\n"
            if ind_2 == 378:
                line = "                  \"name\": \"" + str(raster_name[2]) + "\",\n"

        json_out_playlist0.write(line)
        ind_2 += 1
    json_playlist0.close()
    json_out_playlist0.close()


def find_md5(image):
    pic = open(image, 'rb')
    data = pic.read()
    tmp_md5 = hashlib.md5(data)
    md5 = tmp_md5.hexdigest()
    pic.close()
    return md5


def change_to_manual_mode():
    sock = sock_connect(port=16603)
    port = 4096
    send_board(constant.login, sock, port)
    send_board(constant.change_to_manual, sock, port)


def change_to_auto_mode():
    sock = sock_connect(port=16603)
    port = 4096
    send_board(constant.login, sock, port)
    send_board(constant.change_to_auto, sock, port)


def send_board(command, sock, port):
    data_asc = command.encode()
    data_hex = data_asc.fromhex(command)
    sock.send(data_hex)
    resp = sock.recv(port)
    print('SEND: ', data_asc)
    print('RESPONCE: ', resp)

    return resp


def create_auto_bright_array():
    cprint('  Создаём расписание на плату из таблицы восходов/закатов', 'blue')

    wb = load_workbook('C://Users/Гамбоев/Desktop/TOI_prod/TOI_/tcpimage/timetable/tcp_test_z/timing.xlsx')
    sheet = wb.get_sheet_by_name('Лист1')
    list_time = []
    for row in sheet.rows:
        day = time.strftime("%j", time.localtime())
        if int(row[5].value) == int(day):
            for num in range(1, 5):
                dat = str(row[num].value)
                dat_ = str(int(dat[3:5])) + ' ' + str(int(dat[:2]))
                list_time.append(dat_)
    list1 = []
    list_br = ['11', '22', '33', '44']
    for _ in range(4):
        list_board = ['true', '0 ' + list_time[_], list_br[_]]
        list1.append(list_board)
    cprint('    Сформированное расписание: ' + str(list1), 'magenta')
    return list1


def get_tempret(command):
    sock = sock_connect(port=16603)
    port = 4096
    send_board(constant.login, sock, port)
    resp = send_board(command, sock, port)
    resp = str(resp)
    a = resp.split(sep="previewValue", maxsplit=14)
    c = a[10][3:]
    b = a[11][3:]
    cd = c.find('"') - 2
    bd = b.find('"')
    cc = c[:cd]
    bb = b[:bd]
    print('Яркость:', cc, 'lux')
    print('Температура:', bb, 'гр. Цельсия')
    return cc
    # print('22', resp)


def monitor():
    # command = '55aa00e9fe000100ffff0100170000010100005559' # мигает при начале сканирования
    command = '55aa0020fe000100000000000000000b00018056' # activate monitoring

    def split_list(a_list, wanted_parts=1):
        length = len(a_list)
        return [a_list[i * length // wanted_parts: (i + 1) * length // wanted_parts]
                for i in range(wanted_parts)]

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

    # sock = sock_connect(port=16603)
    # port = 4096
    # send_board(constant.login, sock, port)
    # print('11')
    # sock = sock_connect(port=5200)
    # resp = send_board(command, sock, port)
    resp = 'aa5500ef00fe01000b0000000000000b0001ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff5a56'
    a = bytearray(resp)
    # hex шестнадцатиричный формат
    hexadecimal_string_all = a.hex()
    hexadecimal_string = hexadecimal_string_all[36:-68]
    first_part = hexadecimal_string[:192]
    second_part = hexadecimal_string[-192:]

    n = 0
    list_1 = []
    for _ in first_part:
        if n % 2 == 0:
            list_1.append(hexadecimal_string[n: n + 2])
        n += 1

    n = 0
    list_2 = []
    for _ in second_part:
        if n % 2 == 0:
            list_2.append(second_part[n: n + 2])
        n += 1

    senc = split_list(list_2, wanted_parts=3)[2]
    print(senc)
    list_bin = []
    for hex_ in senc:
        binary_string = binascii.unhexlify(hex_)
        list_bin.append(hex_to_binary(hex_))
    print('55', list_bin)

    list_chet = []
    list_nechet = []
    n = 0
    for _ in list_bin:
        if n % 2 == 0:
            list_chet.append(_)
        else:
            list_nechet.append(_[::-1])
        n += 1
    print(list_chet)
    print(list_nechet)
    zor = split_list(list_nechet, wanted_parts=4)
    print('zor', zor)


def main(change_image, auto_bright_mode, manual_bright_mode, input_bright):
    check_unicode = False
    update_bright_image = UpdateBright(input_bright=input_bright, source_path=constant.path)
    k_l = ['images.png']
    if change_image:
        try:
            raster_name = []
            md5_list = []
            pic_size_list = []
            path_output_image = 'C:/TOI_prod/tcpimage/timetable/tcp_test_z/source/output/'
            path_input_image = 'C:/TOI_prod/tcpimage/timetable/tcp_test_z/source/multi_input/'
            for file in k_l:
                raster_name.append(file)
                in_image = os.path.join(path_input_image, file)
                md5 = find_md5(in_image)
                md5_list.append(md5)
                pic_size = os.path.getsize(in_image)
                pic_size_list.append(pic_size)
            path_for_json = 'C:/TOI_prod/tcpimage/timetable/tcp_test_z/source/'
            create_json_plan_list(md5_list, pic_size_list, path_for_json, raster_name)
            for rast in raster_name:
                print(rast, ' 88888888888888888')
                input_path = os.path.join(path_input_image, rast)
                output_path = os.path.join(path_output_image, rast)
                update = UpdateImage(img_name=rast, source_path=path_for_json, in_path=input_path,
                                     out_path=output_path)
                update.run()
            print("Change image success")
        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            print(e)

    if manual_bright_mode:  # True or False
        print('manual_bright_mode')
        if get_current_bright_mode():
            change_to_manual_mode()
        bright_man = current_bright_value_manual()
        if bright_man == input_bright:
            print('Эта яркость уже есть')

        try:
            update_bright_image.set_bright()

        except Exception as e:
            logging.error("Exception occurred", exc_info=True)
            print(e)
            update_bright_image.set_bright()

    if auto_bright_mode:
        list_br = create_auto_bright_array()
        set_auto_br = AutoBright(list_br, check_unicode, constant.default_byte_block)
        try:
            if not get_current_bright_mode():
                change_to_auto_mode()
            set_auto_br.set_auto_bright()
        except Exception as e:
            cprint('    Start exception ZZZ', 'red')
            logging.error("Exception occurred", exc_info=True)
            print(e)
            sock = sock_connect(port=16603)
            port = 4096
            send_board(constant.login, sock, port)
            sleep(5)
            set_auto_br.set_auto_bright()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s : %(message)s', filename='1.txt')
    update_image = True  # смена картинки
    auto_bright = False  # смена режима работы яркости
    manual_bright = False  # изменить значение яркости
    bright = '10'  # яркость
    i = 1
    main(update_image, auto_bright, manual_bright, bright)

