from django.urls import path

from .views import *


urlpatterns = [
    path('', base_view, name='base_view'),
    path('', draw, name='draw')
]
