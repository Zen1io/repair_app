from django import forms
from .models import Application
from catalog.models import Category
from django.contrib.auth.models import User


class ApplicationForm(forms.ModelForm):
    """Сlass implements the form for creating an application."""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Категория"
    )
    master = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True),
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Мастер"
    )

    class Meta:
        model = Application
        fields = ['first_name', 'last_name',
                  'category',
                  'date_of_readiness',
                  'comment', 'master']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_readiness': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'class': 'form-control',
                    'type': 'date'
                }
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Введите комментарий...'
            }),
        }
