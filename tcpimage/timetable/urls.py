from django.urls import path
from .views import main_page, statistic, monitoring, test, pictures, ipconfig
from .views import CreateStand, auto_bright_module, DeleteStand, UpdateStand, delete_image
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('pictures/', pictures,  name='pictures'),
    path('pictures/<int:pk>/', delete_image, name='delete_image'),
    path('auto/', auto_bright_module, name='auto'),
    path('ajax/crud/create/', CreateStand.as_view(), name='crud_ajax_create'),
    path('ajax/crud/delete/', DeleteStand.as_view(), name='crud_ajax_delete'),
    path('ajax/crud/update/', UpdateStand.as_view(), name='crud_ajax_update'),
    path('statistic/', statistic, name='statistic'),
    path('test/', test, name='test'),
    path('ipconfig/', ipconfig, name='ipconfig'),
    path('monitoring/', monitoring, name='monitoring'),
    path('', main_page, name='main'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


