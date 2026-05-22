"""URLS приложения animals."""

from django.urls import path

namespace = 'animals'

urlpatterns = [
    path('', name='home'),
    path('/catalog/', name='catalog'),
    path('/stories/', name='stories'),
    path('/thanks/', name='thanks'),
    path('/animal/<int:pk>/adopt/', name='adopt_request'),
    path('/animal/<int:pk>/', name='animal_detail'),
]
