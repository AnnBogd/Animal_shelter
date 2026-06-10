"""Формы приложения animals."""

from django import forms

from .models import AdoptionRequest


class AdoptionRequestForm(forms.ModelForm):
    """Форма для заявки на знакомство с животным."""

    class Meta:
        model = AdoptionRequest
        fields = ('name', 'phone', 'email', 'comment')
