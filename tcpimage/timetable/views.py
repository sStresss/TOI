import os
import time
from datetime import datetime
from django.shortcuts import redirect
from django.views.generic import View
from django.http import JsonResponse
from .models import BrightTime, Picture, CheckBoxImage, ManualCount, IpConfig
from .forms import PictureForm
import sys
from django.shortcuts import render
from subprocess import run, PIPE
from django.contrib import messages

""" 1 часть работы с яркостью. Отображение и редактирование"""


class CreateStand(View):

    def get(self, request):
        time_bright1 = request.GET.get('time_bright', None)
        bright_count1 = request.GET.get('bright_count', None)
        obj = BrightTime.objects.create(
            time_bright=time_bright1,
            bright_count=bright_count1,
        )
        stand = {
            'id': obj.id,
            'time_bright': obj.time_bright,
            'bright_count': obj.bright_count,
        }
        data = {
            'stand': stand
        }
        return JsonResponse(data)


class DeleteStand(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        BrightTime.objects.get(id=id1).delete()
        data = {
            'deleted': True
        }
        return JsonResponse(data)


class UpdateStand(View):

    def get(self, request):
        id1 = request.GET.get('id', None)
        time_bright1 = request.GET.get('time_bright', None)
        bright_count1 = request.GET.get('bright_count', None)

        obj = BrightTime.objects.get(id=id1)
        obj.time_bright = time_bright1
        obj.bright_count = bright_count1
        obj.save()

        stand = {
            'id': obj.id,
            'time_bright': obj.time_bright,
            'bright_count': obj.bright_count
        }

        data = {
            'stand': stand
        }
        return JsonResponse(data)


def auto_bright_module(request):
    if request.method == "POST":
        if 'schedule_mode' in request.POST:
            schedule_mode = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\schedule_mode.py'], shell=False, stdout=PIPE)
            print(schedule_mode)

        time_field_name = 'time_bright'
        bright_field_name = 'bright_count'
        # obj_timetable = BrightTime.objects.all().order_by('-id')[:4]
        obj_timetable = BrightTime.objects.all()
        timetable_list = []
        for item in obj_timetable:
            time_field_object = BrightTime._meta.get_field(time_field_name)
            time_field_value = time_field_object.value_from_object(item)

            time_field_value = str(time_field_value)
            hours = int(time_field_value[:2])
            minute = int(time_field_value[3:5])
            bright_field_object = BrightTime._meta.get_field(bright_field_name)
            bright_field_value = bright_field_object.value_from_object(item)
            list_item = str(minute) + '|' + str(hours) + '|' + str(bright_field_value)
            timetable_list.append(list_item)
        print(timetable_list)
        auto_out = run([sys.executable,
                        'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\auto_bright.py',
                        str(timetable_list)], shell=False, stdout=PIPE)
        print(auto_out)
    if request.POST.get('manual'):
        save_manual_bright = ManualCount()
        save_manual_bright.manual_count = request.POST.get('manual')
        save_manual_bright.save()
        a = str(save_manual_bright.manual_count)
        out = run([sys.executable,
                   'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\manual_bright.py',
                   a], shell=False, stdout=PIPE)
        print('111111', out)
    # --- ******************************************************************
    now = datetime.now().time()
    obj_timetable = BrightTime.objects.all()
    time_list = []
    bright_list = []
    auto_current = 0
    for item in obj_timetable:
        time_field_object = BrightTime._meta.get_field('time_bright')
        time_field_value = time_field_object.value_from_object(item)
        bright_field_object = BrightTime._meta.get_field('bright_count')
        bright_field_value = bright_field_object.value_from_object(item)
        time_list.append(time_field_value)
        bright_list.append(bright_field_value)
    for i in range(len(time_list)):
        if now > time_list[i]:
            auto_current = bright_list[i]

    field_name = 'manual_count'
    obj = ManualCount.objects.last()
    field_object = ManualCount._meta.get_field(field_name)
    field_value = field_object.value_from_object(obj)
    mode = 'manual'
    context = {
        'schedule': BrightTime.objects.all(),
        'flag': field_value,
        'auto_current': auto_current,
        'mode': mode
    }
    return render(request, 'timetable/auto.html', context)


""" 2 часть для работы с картинками. Отображение и удаление"""


def pictures(request):
    if request.method == "POST":
        print('www')
        if request.POST.get('image_list'):
            save_image_list = CheckBoxImage()
            print('let_image', save_image_list.image_list)
            save_image_list.image_list = request.POST.get('image_list')
            save_image_list.save()
            print('in_zor_image1', save_image_list.image_list)
            inp = str(save_image_list.image_list)
            print('inp +++++++', inp)
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\change_image.py',
                       inp], shell=False, stdout=PIPE)
            print('111111', out)
        form = PictureForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
    if request.method == "DELETE":
        form = PictureForm(request.DELETE, request.FILES)

    form = PictureForm()
    pic = Picture.objects.all
    print(pic, 'tut')
    return render(request, 'timetable/pictures.html', {'pic': pic, 'form': form})


def add_pictures(request):
    if request.method == 'POST':
        img = request.POST.getlist('checked')
        print(img)


def delete_image(request, pk):
    if request.method == 'POST':
        img = Picture.objects.get(pk=pk)
        img.delete()
    return redirect('pictures')


""" 3 часть для работы с тестированием платы. Панель управления"""


def ipconfig(request):
    if request.method == "POST":
        save_ip_config = IpConfig()
        if 'on_display' in request.POST:
            input_ip = request.POST.get('ip')
            save_ip_config.ip = request.POST.get('ip')

            input_mask = request.POST.get('mask')
            save_ip_config.mask = request.POST.get('mask')

            input_gateway = request.POST.get('gateway')
            save_ip_config.gateway = request.POST.get('gateway')

            save_ip_config.save()
            print('ip', input_ip)
            print('mask', input_mask)
            print('gateway', input_gateway)

    ip_name = 'ip'
    mask_name = 'mask'
    gateway_name = 'gateway'
    obj = IpConfig.objects.last()

    field_object_ip = IpConfig._meta.get_field(ip_name)
    field_value_ip = field_object_ip.value_from_object(obj)

    field_object_mask = IpConfig._meta.get_field(mask_name)
    field_value_mask = field_object_mask.value_from_object(obj)
    sum_mask = 0
    if field_value_mask == "255.255.255.255":
        sum_mask = 32
    if field_value_mask == "255.255.255.254":
        sum_mask = 31
    if field_value_mask == "255.255.255.252":
        sum_mask = 30
    if field_value_mask == "255.255.255.248":
        sum_mask = 29
    if field_value_mask == "255.255.255.240":
        sum_mask = 28
    if field_value_mask == "255.255.255.224":
        sum_mask = 27
    if field_value_mask == "255.255.255.192":
        sum_mask = 26
    if field_value_mask == "255.255.255.128":
        sum_mask = 25
    if field_value_mask == "255.255.255.0":
        sum_mask = 24

    print('sum_mask ', sum_mask)


    field_object_gateway = IpConfig._meta.get_field(gateway_name)
    field_value_gateway = field_object_gateway.value_from_object(obj)

    context = {
        'ip': field_value_ip,
        'mask': field_value_mask,
        'gateway': field_value_gateway,
    }

    set = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'settings.py')
    set2 = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx',
                             'settings2.py')
    gun = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx',
                       'gunicorn_config.py')
    gun2 = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx',
                        'gunicorn_config2.py')
    tcp = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'tcpimage')
    tcp2 = os.path.join('C://TOI_prod/tcpimage/timetable/templates/timetable/change_file_from_nginx', 'tcpimage2')

    with open(set2, 'w') as \
            write_settings:
        with open(set, 'r') as read:
            for line in read:
                if 'ALLOWED_HOST' in line:
                    line = "ALLOWED_HOSTS = ['" + field_value_ip + "']\r"
                write_settings.write(line)

    with open(gun2, 'w') as write_gunicorn:
        with open(gun, 'r') as read:
            for line in read:
                if 'bind' in line:
                    line = "bind = '" + field_value_ip + ":8000'\r"
                write_gunicorn.write(line)

    with open(tcp2, 'w') as write_tcpimage:
        with open(tcp, 'r') as read:
            for line in read:
                # print(line)
                if 'server_name' in line:
                    line = "	server_name " + field_value_ip + ";\r"
                if 'proxy_pass' in line:
                    line = "	proxy_pass http://" + field_value_ip + ":8000;\r"
                write_tcpimage.write(line)

    os.remove(tcp)
    os.remove(gun)
    os.remove(set)

    os.rename(tcp2, tcp)
    os.rename(gun2, gun)
    os.rename(set2, set)

    return render(request, 'timetable/ipconfig.html', context)


def test(request):
    if request.method == "POST":
        if 'on_display' in request.POST:
            print('on_display')
            inp = 'on_display'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            messages.add_message(request, messages.INFO, "Экран включен")
        if 'off_display' in request.POST:
            print('off_display')
            inp = 'off_display'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            messages.add_message(request, messages.INFO, "Экран выключен")
        if 'white' in request.POST:
            print('white')
            inp = 'white'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\change_image_for_test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            messages.add_message(request, messages.INFO, "Цвет изменён на белый")
        if 'red' in request.POST:
            print('red')
            inp = 'red'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\change_image_for_test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            messages.add_message(request, messages.INFO, "Цвет изменён на красный")
        if 'blue' in request.POST:
            print('blue')
            inp = 'blue'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\change_image_for_test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            messages.add_message(request, messages.INFO, "Цвет изменён на синий")
        if 'green' in request.POST:
            print('green')
            inp = 'green'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\change_image_for_test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            messages.add_message(request, messages.INFO, "Цвет изменён на зелёный")
        if 'back_display' in request.POST:
            print('back_display')
            inp = 'back_display'
            out = run([sys.executable,
                       'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\test.py',
                       inp], shell=False, stdout=PIPE)
            print(out)
            # messages.add_message(request, messages.INFO, "Цвет изменён на зелёный")

    return render(request, 'timetable/test.html')


""" 4 часть для главной страницы"""

'/root/TOI_API/tcpimage/timetable/tcp_test_z/manual_bright.py'


def main_page(request):
    temp = 7
    out = run([sys.executable,
               'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\temperature.py'], shell=False, stdout=PIPE)
    print(str(out))
    str_out = str(out)
    l = len(str_out)
    integ = []
    i = 0
    while i < l:
        s_int = ''
        a = str_out[i]
        while '0' <= a <= '9':
            s_int += a
            i += 1
            if i < l:
                a = str_out[i]
            else:
                break
        i += 1
        if s_int != '':
            integ.append(int(s_int))

    print(integ[3])

    context = {
        'temp': integ[3],
    }
    return render(request, 'timetable/main.html', context)


""" 5 часть для отображения статистики"""


def statistic(request):
    if request.method == "POST":
        print('statistic')
        inp = 'statistic'
        out = run([sys.executable,
                   'C:\\TOI_prod\\tcpimage\\timetable\\tcp_test_z\\statistic.py',
                   inp], shell=False, stdout=PIPE)
        print(out)
    context = {
        'proc': '17%',
        'memory': '31%',
    }
    return render(request, 'timetable/statistic.html', context)


""" 6 часть для отображения мониторинга платы"""


def monitoring(request):
    cab = [1, 3, 5, 2, 4, 6, 7, 9, 11, 8, 10, 12]
    pod_cab = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25]
    flag_m = 'start'
    context = {
        'cab': cab,
        'pod_cab': pod_cab,
        'flag_m': flag_m,
    }
    if request.method == "POST":
        return render(request, 'timetable/monitoring.html', context)
    else:
        return render(request, 'timetable/monitoring.html', context)


