"""View-функции приложения animals."""

from django.conf import settings
from django.core.mail import EmailMessage
from django.db.models import QuerySet
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from .forms import AdoptionRequestForm
from .models import AdoptionRequest, Animal


class ReadableEmailMessage(EmailMessage):
    """Кастомный класс письма, который не шифрует русский текст.

    Удалить в релизе.
    """

    def message(self):
        msg = super().message()
        if 'Content-Transfer-Encoding' in msg:
            del msg['Content-Transfer-Encoding']
        return msg


class HomeView(TemplateView):
    """CBV для отображения главной страницы."""

    template_name = 'animals/home.html'

    def get_context_data(self, **kwargs) -> dict:
        """Дополнить словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['shelter_count'] = (
            Animal
            .objects
            .filter(status='shelter')
            .count()
        )
        context['adopted_count'] = (
            Animal
            .objects
            .filter(status='adopted')
            .count()
        )
        context['recent_animals'] = (
            Animal
            .objects
            .filter(status='shelter')
            .order_by('-arrival_date')[:3])
        return context


class BaseAnimalListView(ListView):
    """Базовый CBV для отображения списка животных."""

    model = Animal
    paginate_by = 6
    context_object_name = 'animals'

    def get_queryset(self) -> QuerySet[Animal]:
        """Дополнить queryset фильрацией по имени или виду животного."""
        queryset = super().get_queryset()
        species = self.request.GET.get('species')
        if species:
            queryset = queryset.filter(species=species)
        name = self.request.GET.get('q')
        if name:
            queryset = queryset.filter(name__icontains=name)
        return queryset

    def get_context_data(self, **kwargs) -> dict:
        """Дополнить словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        context['species_choices'] = Animal.ANIMAL_CHOICES
        return context


class ShelterAnimalListView(BaseAnimalListView):
    """CBV для отображения животных, находящихся в приюте."""

    template_name = 'animals/animal_list.html'

    def get_queryset(self) -> QuerySet[Animal]:
        """Дополнить queryset фильрацией - находится в приюте."""
        return super().get_queryset().filter(status='shelter')


class AdoptedAnimalListView(BaseAnimalListView):
    """CBV для отображения животных, которых забрали домой."""

    template_name = 'animals/adopted_list.html'

    def get_queryset(self) -> QuerySet[Animal]:
        """Дополнить queryset фильрацией - забрали домой, с сортировкой."""
        queryset = super().get_queryset()
        return queryset.filter(status='adopted').order_by('-adoption_date')


class AnimalDetailView(DetailView):
    """CBV для отображения отдельной страницы животного."""

    model = Animal
    template_name = 'animals/animal_detail.html'

    def get_context_data(self, **kwargs) -> dict:
        """Дополнить словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['next'] = self.request.GET.get('next', '')
        context['anchor'] = self.request.GET.get('anchor', '')
        return context


class AdoptRequestCreateView(CreateView):
    """CBV для отображения заявок."""

    model = AdoptionRequest
    form_class = AdoptionRequestForm
    success_url = reverse_lazy('animals:thanks')
    template_name = 'animals/adopt_request_form.html'

    def get_animal(self) -> Animal:
        """Получить животное, на которое оформляется заявка."""
        if not hasattr(self, '_animal'):
            self._animal = get_object_or_404(Animal, pk=self.kwargs['pk'])
        return self._animal

    def form_valid(self, form: AdoptionRequestForm) -> HttpResponseRedirect:
        """Привязать животное к форме и отправить админу email."""
        form.instance.animal = self.get_animal()
        response = super().form_valid(form)
        self.send_notification_email(form)
        return response

    def send_notification_email(self, form):
        """Отправить админу email о созданной заявке."""

        adoption_request = form.instance
        animal = adoption_request.animal
        email = ReadableEmailMessage(
            subject=f'Новая заявка на {animal.name}',
            body=f'''
Поступила новая заявка на знакомство:
Животное: {animal.name} ({animal.get_species_display()})
Имя пользователя: {adoption_request.name}
Телефон пользователя: {adoption_request.phone}
Email пользователя: {adoption_request.email}
Комментарий: {adoption_request.comment}
''',
            from_email='noreply@example.com',
            to=[settings.ADMIN_EMAIL],
        )
        email.encoding = 'utf-8'
        email.send(fail_silently=True)

    def get_context_data(self, **kwargs) -> dict:
        """Дополнить словарь контекста."""
        context = super().get_context_data(**kwargs)
        context['animal'] = self.get_animal()
        return context
