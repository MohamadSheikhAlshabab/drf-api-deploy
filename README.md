# drf-api-deploy

## in the terminal

- mkdir 'some folder name'
- cd 'some folder name '
- poetry init -n
- poetry shell
- poetry add django djangorestframework gunicorn whitenoise djangorestframework_simplejwt django-cors-headers psycopg2-binary django-environ
- poetry add --dev black
- django-admin startproject 'project_name_project' . (don't forget the dot)
- python manage.py startapp 'app_name'
- python manage.py createsuperuser
- python manage.py makemigrations "app_name"
- python manage.py migrate
- python manage.py runserver
- poetry export -f requirements.txt -o requirements.txt
- docker-compose up -d --build
- docker-compose exec web python manage.py migrate
---
- project/sample.py

                                DEBUG=on
                                SECRET_KEY=cg8=^m)dp74_(42r!hhr6x)umzo^ted#+%2*)6r=_-e31evy3v
                                DATABASE_NAME=postgres
                                DATABASE_USER=postgres
                                DATABASE_PASSWORD=put-real-db-password-here
                                DATABASE_HOST=db
                                DATABASE_PORT=5432
                                ALLOWED_HOSTS=localhost,127.0.0.1

---

## Project

- projct/settings.py

                import os

                env = environ.Env(
                    DEBUG = (bool, False)
                )

                environ.Env.read_env()
                SECRET_KEY = env.str('SECRET_KEY')

                DEBUG = env.bool('DEBUG')

                ALLOWED_HOSTS = ['0.0.0.0','127.0.0.1','localhost']

                INSTALLED_APPS = [
                   'rest_framework',
                    'corsheaders',
                    'python.apps.PythonConfig',
                ]
                MIDDLEWARE = ['whitenoise.middleware.WhiteNoiseMiddleware',]
                DATABASES = {
                    'default': {
                        'ENGINE': 'django.db.backends.postgresql',
                        'NAME': env.str('DATABASE_NAME'),
                        'USER': env.str('DATABASE_USER'),
                        'PASSWORD': env.str('DATABASE_PASSWORD'),
                        'HOST': env.str('DATABASE_HOST'),
                        'PORT': env.str('DATABASE_PORT')
                    }
                }
                STATIC_DIR = os.path.join(BASE_DIR, 'static')
                STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
                STATIC_URL = '/static/'
                STATICFILES_DIRS = [
                    STATIC_DIR,
                ]

                REST_FRAMEWORK = {
                    'DEFAULT_PERMISSION_CLASSES': [
                        'rest_framework.permissions.IsAuthenticated',
                    ],
                    'DEFAULT_AUTHENTICATION_CLASSES':[
                        'rest_framework_simplejwt.authentication.JWTAuthentication',
                        'rest_framework.authentication.SessionAuthentication',
                        'rest_framework.authentication.BasicAuthentication',
                    ]
                }


                CORS_ORIGIN_WHITELIST = [
                    'http://localhost:3000',
                ]
                
---
- project/urls.py

                  from django.contrib import admin
                  from django.urls import path,include
                  from rest_framework_simplejwt import views as jwt_views

                  urlpatterns = [
                      path('admin/', admin.site.urls),
                      path('api/v1/',include('python.urls')),
                      path('api-auth', include('rest_framework.urls')),
                      path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
                      path('api/token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),

                  ]
                  
---

## APP

- app/admin.py

                from django.contrib import admin
                from .models import Python
                admin.site.register(Python)
                
---
- app/models.py

              from django.db import models
              from django.contrib.auth import get_user_model

              # Create your models here.

              class Python(models.Model):
                  programmer = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
                  glossary  = models.BooleanField()
                  simple = models.BooleanField()
                  user_friendly = models.BooleanField()
                  GUI = models.BooleanField()

                  def __str__(self):
                      return str(self.programmer)
                      
---

- app/permissions.py

        from rest_framework import permissions

        class IsProgrammerOrReadOnly(permissions.BasePermission):
            def has_object_permission(self, request, view, obj):
                if request.method in permissions.SAFE_METHODS:
                    return True
                return obj.programmer == request.user
                
---

- app/serializer.py

                from rest_framework import serializers
                from .models import Python

                class PythonSerializer(serializers.ModelSerializer):
                    class Meta:
                        fields = ('programmer','glossary','simple','user_friendly','user_friendly')
                        model = Python
                        
---

- app/urls.py

                          from django.urls import path
                          from .views import PythonList , PythonDetails

                          urlpatterns = [
                              path('python',PythonList.as_view(), name='python_list'),
                              path('python/<int:pk>',PythonDetails.as_view(), name='python_details'),
                          ]
                          
---

- app/views.py

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
---

## ROOT

- docker-compose.yml

                              version: '3'
                              services:
                                  web:
                                      build: .
                                      # command: python manage.py runserver 0.0.0.0:8000
                                      command: gunicorn programs.wsgi:application --bind 0.0.0.0:8007 --workers 4
                                      volumes:
                                          - .:/code
                                      ports:
                                          - "8007:8007"

                                      depends_on:
                                          - db
                                  db:
                                      image: postgres:11
                                      environment:
                                          - "POSTGRES_HOST_AUTH_METHOD=trust"
                                          
---

- Dockerfile

                                FROM python:3
                                ENV PYTHONDONTWRITEBYTECODE 1
                                ENV PYTHONUNBUFFERED 1
                                RUN mkdir /code
                                WORKDIR /code
                                COPY requirements.txt /code/
                                RUN pip install -r requirements.txt
                                COPY . /code/
---

