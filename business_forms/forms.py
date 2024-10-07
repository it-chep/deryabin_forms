from django import forms
from business_forms.models import UltimaRequest


class UltimaRequestForm(forms.ModelForm):
    """Форма запроса с полями для инвестиций"""
    currency = forms.MultipleChoiceField(
        choices=UltimaRequest.CURRENCY_CHOICES,
        widget=forms.SelectMultiple(attrs={
            'placeholder': 'Выберите валюту инвестирования',
            'id': 'id_currency',
        }),
        required=False,
        label="Укажите валюту инвестирования (можно отметить несколько вариантов):"
    )

    class Meta:
        model = UltimaRequest
        fields = (
            "name",
            "phone",
            "city",
            "currency",
            "age",
            "investment_goal",
            "investment_period",
            "available_sum",
            "additional_question",
        )
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Введите ваше имя'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Введите ваш номер телефона'}),
            'city': forms.TextInput(attrs={'placeholder': 'Введите ваш город'}),
            'age': forms.RadioSelect,
            'investment_goal': forms.RadioSelect,
            'investment_period': forms.RadioSelect,
            'available_sum': forms.RadioSelect,
            'additional_question': forms.TextInput(attrs={'placeholder': 'Можете задать любой вопрос'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'additional_question':
                field.required = True

        self.fields['age'].choices = list(UltimaRequest.AGE_CHOICES)
        self.fields['investment_goal'].choices = list(UltimaRequest.INVESTMENT_GOAL_CHOICES)
        self.fields['investment_period'].choices = list(UltimaRequest.INVESTMENT_PERIOD_CHOICES)
        self.fields['available_sum'].choices = list(UltimaRequest.SAVINGS_CHOICES)