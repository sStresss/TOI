from django.contrib import admin

from .models import MainPage, Picture, chkboxcourse, CheckBoxImage


class BrightTableAdmin(admin.ModelAdmin):
    list_display = ('time', 'bright', 'enable')
    list_display_links = ('time', 'bright')
    search_fields = ('time', 'bright')


@admin.register(Picture)
class PictureAdmin(admin.ModelAdmin):
    list_display = ['id', 'photo', 'date']


admin.site.register(chkboxcourse)
admin.site.register(CheckBoxImage)

admin.site.register(MainPage)


