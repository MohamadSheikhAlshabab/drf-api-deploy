from django.urls import path
from .views import PythonList , PythonDetails

urlpatterns = [
    path('python',PythonList.as_view(), name='python_list'),
    path('python/<int:pk>',PythonDetails.as_view(), name='python_details'),
]