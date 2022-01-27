import socket
import sys
import time
import constant
import logging
import toi_connect
from collections import Counter
from time import sleep
from termcolor import cprint
from openpyxl import load_workbook
import schedule



class AutoBright:
    def __init__(self, list_bright):
        self.auto_bright_array = []
        self.check_unicode = False
        self.default_byte_block = constant.default_byte_block  # Байтовые строки в константте
        self.start_delta = 0
        self.time_data = ''
        self.socket = self.sock_connect(port=16603)
        self.path_xlsx = constant.path_to_table_bright_xlsx
        self.port = 4096
        self.list_bright = list_bright

    def set_auto_bright(self):
        cprint('старт изменения авто-яркости', 'yellow')

        self.send_board(constant.login_image)
        self.auto_bright_array = self.create_auto_bright_array()

        len_arr = len(self.auto_bright_array)

        self.send_board(constant.login)

        # считаем дельту смещения
        self.start_delta = self.find_delta()
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

        self.socket.send(data_1)
        bright_resp = str(self.socket.recv(512))  # Добавить в лог
        #if len(bright_resp) < 4 or 'password' in bright_resp:
        #    raise Exception("    bad answer")
        cprint('    Ответ от платы: ' + bright_resp, 'green')
        self.socket.close()
        cprint('авто-яркость успешно изменена', 'yellow')
        print('авто-яркость успешно изменена')

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

    def get_current_bright_mode(self):
        mode = self.current_mode_bright()
        if mode:
            self.current_bright_value_auto()
            return True
        if not mode:
            return False

    def current_mode_bright(self):
        # Получаем ответ по режиму яркости на плате auto|manual
        cprint('  Получаем ответ по режиму яркости на плате auto|manual', 'blue')
        resp = self.send_board(constant.mode)
        resp = str(resp)

        resp_split = resp.split('}],"enable":', 1)
        resp_ = resp_split[1][:5]
        print('RESP_: ', resp_)
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

    def current_bright_value_auto(self):

        resp = self.send_board(constant.bright_auto_mode)
        resp = str(resp)
        resp_ = self.send_board(constant.check_manual_bright)
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

    def sock_connect(self, port):
        sock = socket.socket()
        sock.connect((constant.hostIP, port))
        return sock

    def change_to_auto_mode(self):
        self.send_board(constant.change_to_auto)

    def send_board(self, command):
        data_asc = command.encode()
        data_hex = data_asc.fromhex(command)
        self.socket.send(data_hex)
        resp = self.socket.recv(self.port)
        return resp

    def create_auto_bright_array(self):
        cprint('  Создаём расписание на плату из таблицы восходов/закатов', 'blue')
        wb = load_workbook(self.path_xlsx)
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

        for _ in range(4):
            list_board = ['true', '0 ' + list_time[_], self.list_bright[_]]
            list1.append(list_board)
        cprint('    Сформированное расписание: ' + str(list1), 'magenta')
        return list1


def amount_of_brightness():
    sock = toi_connect.sock_connect(buffer=16603)
    buffer = 4096
    toi_connect.send_board(constant.login, sock, buffer)
    resp = toi_connect.send_board(constant.temperature_bright, sock, buffer)
    resp = str(resp)
    a = resp.split(sep="previewValue", maxsplit=14)
    c = a[10][3:]
    cd = c.find('"') - 2
    cc = c[:cd]
    print('Яркость:', cc, 'lux')
    return int(cc)


def main(list_bright):
    bright_count = amount_of_brightness()
    if bright_count > 4000:
        list_change = []
        for _ in list_bright:
            item = int(_) + 1
            list_change.append(str(item))
        AutoBright(list_change)

    set_auto_br = AutoBright(list_bright)
    try:
        set_auto_br.set_auto_bright()
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print(e)
        sleep(5)
        set_auto_br.set_auto_bright()


def job():
    print('im  working')


if __name__ == "__main__":
    list_bright_count = ['1', '2', '3', '4']
    schedule.every(1).seconds.do(job)
    while True:
        schedule.run_pending()

    # for _ in range(100):
    #
    #     # main(list_bright_count)
    #     time.sleep(100)
