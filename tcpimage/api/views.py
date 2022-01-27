from django.shortcuts import render
from rest_framework import generics
from . import serialisers

from .models import Cabinets, Modules, ColorPixel


class CabinetList(generics.ListCreateAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = serialisers.CabinetSerializer


class CabinetDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = serialisers.CabinetSerializer


class CabinetDepthAPIView(generics.ListAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = serialisers.CabinetDepthSerializer


class ModulesList(generics.ListCreateAPIView):
    queryset = Modules.objects.all()
    serializer_class = serialisers.ModuleSerializer


class ModulesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Modules.objects.all()
    serializer_class = serialisers.ModuleSerializer


class ColorPixelList(generics.ListCreateAPIView):
    queryset = ColorPixel.objects.all()
    serializer_class = serialisers.ColorPixelSerializer


class ModulesNestedDetail(generics.ListAPIView):
    queryset = Cabinets.objects.all()
    serializer_class = serialisers.CabinetNestedSerializer

