from django.db import models


class Cabinets(models.Model):
    item = models.CharField(max_length=100, verbose_name='Номер кабинета')
    number_of_broken = models.CharField(max_length=100, null=True, verbose_name='Битых пикселей')
    percent_broken = models.CharField(max_length=100, null=True, verbose_name='Процент битых пикселей')
    # skill = models.ManyToManyField('Modules', verbose_name='Модуль', related_name='cabinets')
    # module = models.ForeignKey('Modules', related_name='cabinets', on_delete=models.CASCADE, null=True)


class Modules(models.Model):
    item_module = models.CharField(max_length=100, verbose_name='Номер модуля')
    module_broken = models.CharField(max_length=100, null=True, verbose_name='Процент битых пикселей')
    # red_module = models.CharField(max_length=10000)
    # green_module = models.CharField(max_length=10000)
    # blue_module = models.CharField(max_length=10000)
    cabinet = models.ForeignKey('Cabinets', related_name='modules', on_delete=models.CASCADE, null=True,
                                verbose_name='Номер кабинета')

    class Meta:
        ordering = ['item_module']


class ColorPixel(models.Model):
    red_module = models.CharField(max_length=10000)
    green_module = models.CharField(max_length=10000)
    blue_module = models.CharField(max_length=10000)
    module = models.ForeignKey('Modules', related_name='color_pixel', on_delete=models.CASCADE, null=True)
