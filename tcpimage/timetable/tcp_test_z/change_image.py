import socket
import os
import hashlib
import shutil
import constant
import logging
import sys


class UpdateImage:

    def __init__(self, images):
        self.source_path = os.path.join(constant.project_path, 'timetable/tcp_test_z/source/')
        self.in_path = os.path.join(constant.project_path, 'media/myimage/')
        self.out_path = os.path.join(constant.project_path, 'timetable/tcp_test_z/source/output/')
        self.data_list = constant.list_plat
        self.input_image_list = images
        self.raster_name = []
        self.md5_list = []
        self.pic_size_list = []
        self.list_json = constant.list_json
        self.response = ''
        self.host = constant.hostIP

    def run(self):
        # Создаём 2 json-на в зависимости от количества картинок
        self.create_json_plan_list()

        # Логин на плату командой login_image
        socket_object = self.sock_connect(port=16603)
        port = 4096
        self.send_board(constant.login_image, socket_object, port)

        # Создаём ftp-сокет
        sock_ftp = self.sock_connect(port=16602)

        # Отправляем json-ы на плату
        self.connect_board(sock_ftp)
        for json_item in self.list_json:
            self.send_json_to_board(sock_ftp, json_item)

        # Отправляем картинки на плату
        for image in self.input_image_list:
            in_image_path = self.in_path + image
            # Считаем md5-хэш картинки
            md5_hash = self.calculate_md5_hash_image(in_image_path)

            out_image_path = self.out_path + image

            # копируем картинку с родным именем
            shutil.copyfile(in_image_path, out_image_path)

            # копируем картинку с md5 именем
            md5output_path = self.source_path + '/output/' + str(md5_hash) + '.png'
            shutil.copyfile(in_image_path, md5output_path)

            # отправляем картинку в каталог проекта
            self.send_image_board_project(sock_ftp, md5_hash, image)

            # отправляем картинку в каталог медиа
            self.send_image_board_media(md5_hash, sock_ftp, image)

        port = 1024
        self.send_board(constant.login, socket_object, port)
        # Загружаем проект
        self.send_board(constant.run_hard, socket_object, port)

    def send_json_to_board(self, sock, json_item):
        data = "PASV\n".encode()
        sock.sendall(data)
        resp2 = sock.recv(1024)
        ftp_data_port = self.find_port_value(str(resp2))
        data_ = "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-24/1/" + json_item + "\n"
        data = data_.encode()
        sock.sendall(data)
        sock.recv(1024)
        data_sock = self.sock_connect(port=ftp_data_port)
        output_json = os.path.join(self.source_path + '/output/' + json_item)
        f = open(output_json, 'rb')
        file_size = os.path.getsize(output_json)
        data = f.read(file_size)
        data_sock.send(data)
        data_sock.close()
        sock.recv(1024)

    def thread_img_load(self, data_port, img_name):
        sock = self.sock_connect(port=data_port)
        f = open(self.source_path + '/output/' + img_name, 'rb')
        while True:
            line = f.readline(512)
            if not line:
                break
            sock.send(line)
        sock.close()

    def send_image_board_media(self, md5, sock, img_name):
        data = "PASV\n".encode()
        sock.sendall(data)
        resp_port = sock.recv(128)
        data = "STOR sdcard/nova/viplex_terminal/media/" + md5 + ".png\n"
        data = data.encode()
        sock.sendall(data)
        sock.recv(128)
        ftp_data_port = self.find_port_value(str(resp_port))
        self.thread_img_load(ftp_data_port, img_name)
        sock.recv(1024)

    def send_image_board_project(self, sock, md5, img_name):
        data = "PASV\n".encode()
        sock.sendall(data)
        resp_port = sock.recv(128)
        data = "STOR sdcard/nova/viplex_terminal/program/program_SINAPS-NOUT-24/1/" + md5 + ".png\n"
        data = data.encode()
        sock.sendall(data)
        sock.recv(128)
        ftp_data_port = self.find_port_value(str(resp_port))
        self.thread_img_load(ftp_data_port, img_name)
        sock.recv(1024)

    def find_port_value(self, value):
        print(self.source_path)
        value_split = value.split(sep=",", maxsplit=5)
        value_split_2 = str(value_split[5]).find(")")
        port_num = int(value_split[4]) * 256 + int(value_split[5][0:value_split_2])
        return port_num

    def connect_board(self, sock):
        sock.recv(1024)
        for _ in range(6):
            data = self.data_list[_].encode()
            sock.sendall(data)
            sock.recv(1024)

    def calculate_md5_hash_image(self, image_):
        print(self.source_path)
        pic = open(image_, 'rb')
        data = pic.read()
        tmp_md5 = hashlib.md5(data)
        md5 = tmp_md5.hexdigest()
        pic.close()
        return md5

    def create_json_plan_list(self):
        for file in self.input_image_list:
            self.raster_name.append(file)
            in_image = os.path.join(self.in_path, file)
            md5 = self.calculate_md5_hash_image(in_image)
            self.md5_list.append(md5)
            pic_size = os.path.getsize(in_image)
            self.pic_size_list.append(pic_size)
        # Удаляем файлы из output_catalog
        self.clear_output_catalog()

        json_plan_list = 0
        json_playlist0 = 0
        if len(self.md5_list) == 1:
            json_plan_list = open(self.source_path + '/planlist1.json', 'r')
            json_playlist0 = open(self.source_path + '/playlist0_1.json', 'r')
        if len(self.md5_list) == 2:
            json_plan_list = open(self.source_path + 'planlist2.json', 'r')
            json_playlist0 = open(self.source_path + 'playlist0_2.json', 'r')
        if len(self.md5_list) == 3:
            json_plan_list = open(self.source_path + 'planlist3.json', 'r')
            json_playlist0 = open(self.source_path + 'playlist0_3.json', 'r')

        json_out_plan_list = open(self.source_path + '/output/planlist.json', "a", encoding='utf8')
        ind = 1

        for line in json_plan_list:
            if ind == 34:
                line = '      \"fileName\": \"' + str(self.md5_list[0]) + '.png\",\n'
            if ind == 35:
                line = '      \"md5\": \"' + str(self.md5_list[0]) + '\",\n'
            if ind == 37:
                line = '      "size": ' + str(self.pic_size_list[0]) + '\n'

            if len(self.md5_list) == 2 or len(self.md5_list) == 3:
                if ind == 40:
                    line = '      \"fileName\": \"' + str(self.md5_list[1]) + '.png\",\n'
                if ind == 41:
                    line = '      \"md5\": \"' + str(self.md5_list[1]) + '\",\n'
                if ind == 43:
                    line = '      "size": ' + str(self.pic_size_list[1]) + '\n'
            if len(self.md5_list) == 3:
                if ind == 46:
                    line = '      \"fileName\": \"' + str(self.md5_list[2]) + '.png\",\n'
                if ind == 47:
                    line = '      \"md5\": \"' + str(self.md5_list[2]) + '\",\n'
                if ind == 49:
                    line = '      "size": ' + str(self.pic_size_list[2]) + '\n'

            json_out_plan_list.write(line)
            ind += 1
        json_plan_list.close()
        json_out_plan_list.close()
        json_out_playlist0 = open(self.source_path + '/output/playlist0.json', "a", encoding='utf8')
        ind_2 = 1

        for line in json_playlist0:
            if ind_2 == 94:
                line = "                  \"filesize\": " + str(self.pic_size_list[0]) + ",\n"
            if ind_2 == 97:
                line = "                  \"dataSource\": \"" + str(self.md5_list[0]) + ".png\",\n"
            if ind_2 == 101:
                line = "                  \"name\": \"" + str(self.raster_name[0]) + "\",\n"

            if len(self.md5_list) == 2:
                if ind_2 == 233:
                    line = "                  \"filesize\": " + str(self.pic_size_list[1]) + ",\n"
                if ind_2 == 236:
                    line = "                  \"dataSource\": \"" + str(self.md5_list[1]) + ".png\",\n"
                if ind_2 == 240:
                    line = "                  \"name\": \"" + str(self.raster_name[1]) + "\",\n"

            if len(self.md5_list) == 3:
                if ind_2 == 232:
                    line = "                  \"filesize\": " + str(self.pic_size_list[1]) + ",\n"
                if ind_2 == 235:
                    line = "                  \"dataSource\": \"" + str(self.md5_list[1]) + ".png\",\n"
                if ind_2 == 239:
                    line = "                  \"name\": \"" + str(self.raster_name[1]) + "\",\n"

                if ind_2 == 371:
                    line = "                  \"filesize\": " + str(self.pic_size_list[2]) + ",\n"
                if ind_2 == 374:
                    line = "                  \"dataSource\": \"" + str(self.md5_list[2]) + ".png\",\n"
                if ind_2 == 378:
                    line = "                  \"name\": \"" + str(self.raster_name[2]) + "\",\n"

            json_out_playlist0.write(line)
            ind_2 += 1
        json_playlist0.close()
        json_out_playlist0.close()

    def sock_connect(self, port):
        sock = socket.socket()
        sock.connect((self.host, port))
        return sock

    def clear_output_catalog(self):
        for file_object in os.listdir(self.out_path):
            file_object_path = os.path.join(self.out_path, file_object)
            if os.path.isfile(file_object_path):
                os.unlink(file_object_path)
            else:
                shutil.rmtree(file_object_path)

    def send_board(self, command, sock, port):
        data_asc = command.encode()
        data_hex = data_asc.fromhex(command)
        sock.send(data_hex)
        self.response = sock.recv(port)


def main(image_list):
    try:
        update = UpdateImage(image_list)
        update.run()
        print("Change image success")
    except Exception as e:
        logging.error("Exception occurred", exc_info=True)
        print(e)


if __name__ == "__main__":
    images = sys.argv[1]
    list_input_image = []
    for image in images.split(', '):
        image_now = image[8:].replace(',', '')
        list_input_image.append(image_now)
    print(list_input_image)
    main(list_input_image)
