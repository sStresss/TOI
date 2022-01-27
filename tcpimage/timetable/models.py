from django.db import models


class chkboxcourse(models.Model):
    coursename = models.CharField(max_length=100)


class CheckBoxImage(models.Model):
    image_list = models.CharField(max_length=100)


class ManualCount(models.Model):
    manual_count = models.CharField(max_length=100)


class Picture(models.Model):
    photo = models.ImageField(upload_to='myimage')
    date = models.DateTimeField(auto_now_add=True)

    def delete(self, *args, **kwargs):
        self.photo.delete()
        super().delete(*args, **kwargs)


class MainPage(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Название')


class BrightTime(models.Model):
    time_bright = models.TimeField(max_length=30, blank=True)
    bright_count = models.IntegerField(blank=True)


class IpConfig(models.Model):
    ip = models.CharField(max_length=16)
    mask = models.CharField(max_length=16)
    gateway = models.CharField(max_length=16)