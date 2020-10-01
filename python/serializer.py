from rest_framework import serializers
from .models import Python

class PythonSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('programmer','glossary','simple','user_friendly','user_friendly')
        model = Python