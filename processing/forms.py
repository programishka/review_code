from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from extension_user.models import validate_inn


class TransferMoneyForm(forms.Form):
    user_from = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label="От кого")
    inn_to = forms.CharField(label="Кому", help_text="Введите несколько ИНН через запятую")
    amount = forms.DecimalField(label="Сумма")

    def clean_user_from(self):
        data = self.cleaned_data['user_from']
        return data

    def clean_inn_to(self):
        data = self.cleaned_data['inn_to']
        inns = data.split(',')
        for inn in inns:
            validate_inn(value=inn)

        return data

    def clean(self):
        pass

    def save(self):
        pass
