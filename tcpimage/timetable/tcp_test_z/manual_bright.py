import socket
import os
import shutil
import sys
import constant
import logging
from termcolor import cprint
import toi_connect


class UpdateBright:

    def __init__(self, input_bright):
        self.input_bright = input_bright
        self.socket = self.sock_connect(port=16603)
        self.port = 4096

    def set_bright(self):
        self.send_board(constant.login_image)

        if self.get_current_bright_mode():
            self.change_to_manual_mode()
        bright_man = self.current_bright_value_manual()
        if bright_man == self.input_bright:
            print('Эта яркость уже есть')

        if len(self.input_bright) == 1:
            self.input_bright = '0' + self.input_bright
        if self.input_bright != '100':
            data_0 = 'AVON%\x00\x00\x00QR\x18\x00\x04\x01\x00\x00\x0e\x00\x00\x00\x00\x00\'\x02{"ratio":' \
                     + self.input_bright + '.0}'
        else:
            data_0 = 'AVON\x16\x00\x00\x00QR\x18\x00\x04\x01\x00\x00\x0f\x00\x00\x00\x00\x00\x19\x02{"ratio":100.0}'
        data_0 = data_0.encode()
        self.socket.send(data_0)
        self.socket.recv(4096)
        self.socket.close()

    def get_current_bright_mode(self):
        mode = self.current_mode_bright()
        if mode:
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

    def current_bright_value_manual(self):
        self.send_board(constant.check_manual_bright1)
        resp = self.send_board(constant.check_manual_bright)
        str_resp_z1 = str(resp)
        x = str_resp_z1.split(":", 1)
        x_1 = x[1]
        bright_man = x_1[:x_1.find(".")]
        print('bright current_bright_value_manual: ', bright_man)
        return bright_man

    def sock_connect(self, port):
        sock = socket.socket()
        sock.connect((constant.hostIP, port))
        return sock

    def clear_output_catalog(self, path):
        for file_object in os.listdir(path):
            file_object_path = os.path.join(path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

    def change_to_manual_mode(self):
        self.send_board(constant.change_to_manual)

    def send_board(self, command):
        data_asc = command.encode()
        data_hex = data_asc.fromhex(command)
        self.socket.send(data_hex)
        resp = self.socket.recv(self.port)
        return resp


def main(input_bright):
    update_bright_image = UpdateBright(input_bright=input_bright)

    try:
        update_bright_image.set_bright()
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print(e)
        update_bright_image.set_bright()


if __name__ == "__main__":
    bright = '30'  # яркость
    manual = sys.argv[1]
    print(manual, '00000000000000000')
    main(manual)

