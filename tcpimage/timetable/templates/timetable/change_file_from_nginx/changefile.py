# Allowed_host in settings
# gunicorn_config in host
# sites_avalable nginx
import os
# wb = load_workbook('C://Users/Гамбоев/Desktop/TOI_prod/TOI_/tcpimage/timetable/tcp_test_z/timing.xlsx')

# print(C:\TOI_prod\tcpimage\timetable\tcp_test_z\calculate_pixel\)

path_set = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'settings.py')
path_set2 = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'settings2.py')
gun = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'gunicorn_config.py')
gun2 = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'gunicorn_config2.py')
tcp = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'tcpimage')
tcp2 = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'tcpimage2')

with open(path_set2, 'w') as \
        write_settings:
    with open(path_set, 'r') as read:
        for line in read:
            if 'ALLOWED_HOST' in line:
                line = "ALLOWED_HOSTS = ['192.168.88.000123411']\r"
            write_settings.write(line)

with open(gun2, 'w') as write_gunicorn:
    with open(gun, 'r') as read:
        for line in read:
            if 'bind' in line:
                line = "bind = '192.168.88.000:8000234111'\r"
            write_gunicorn.write(line)

with open(tcp2, 'w') as write_tcpimage:
    with open(tcp, 'r') as read:
        for line in read:
            # print(line)
            if 'server_name' in line:
                line = "	server_name 192.168.88.00023411;\r"
            if 'proxy_pass' in line:
                line = "	proxy_pass http://192.168.88.000:800013241;\r"
            write_tcpimage.write(line)


os.remove(tcp)
os.remove(gun)
os.remove(path_set)
os.rename(tcp2, tcp)
os.rename(gun2, gun)
os.rename(path_set2, path_set)
