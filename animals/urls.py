"""URLS приложения animals."""

from django.urls import path
from django.views.generic import TemplateView

from .views import (
    AdoptRequestCreateView,
    AdoptedAnimalListView,
    AnimalDetailView,
    HomeView,
    ShelterAnimalListView
)

app_name = 'animals'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('catalog/', ShelterAnimalListView.as_view(), name='catalog'),
    path('stories/', AdoptedAnimalListView.as_view(), name='stories'),
    path(
        'thanks/',
        TemplateView.as_view(template_name='animals/thanks.html'),
        name='thanks'
    ),
    path(
        'animal/<int:pk>/adopt/',
        AdoptRequestCreateView.as_view(),
        name='adopt_request'
    ),
    path('animal/<int:pk>/', AnimalDetailView.as_view(), name='animal_detail'),
]
