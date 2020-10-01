from django.shortcuts import render
from rest_framework import generics
from .models import Python
from .serializer import PythonSerializer
from .permissions import IsProgrammerOrReadOnly
from rest_framework import permissions

class PythonList(generics.ListCreateAPIView):
    queryset = Python.objects.all()
    serializer_class = PythonSerializer

class PythonDetails(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsProgrammerOrReadOnly,)
    queryset = Python.objects.all()
    serializer_class = PythonSerializer