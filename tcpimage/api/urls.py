from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('cabinets/', views.CabinetList.as_view()),
    path('cabinets/<int:pk>/', views.CabinetDetail.as_view()),

    path('cabinets/depth/', views.CabinetDepthAPIView.as_view()),
    path('cabinets/nested/', views.ModulesNestedDetail.as_view()),


    path('modules/', views.ModulesList.as_view()),
    path('modules/<int:pk>/', views.ModulesDetail.as_view()),

    path('modules/color/', views.ColorPixelList.as_view())


]

urlpatterns = format_suffix_patterns(urlpatterns)
