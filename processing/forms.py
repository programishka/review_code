from decimal import Decimal, ROUND_DOWN

from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from extension_user.models import validate_inn
from processing.models import Transaction


class TransferMoneyForm(forms.Form):
    user_from = forms.ModelChoiceField(queryset=get_user_model().objects.all(), label="От кого")
    inn_to = forms.CharField(label="Кому", help_text="Введите несколько ИНН через запятую")
    amount = forms.DecimalField(label="Сумма")

    def list_inn_from_value(self, value):
        inns = [v.strip() for v in value.split(',')]
        return inns

    def clean_inn_to(self):
        data = self.cleaned_data['inn_to']
        for inn in self.list_inn_from_value(data):
            validate_inn(value=inn)
            if not get_user_model().objects.filter(inn=inn).exists():
                raise ValidationError(
                    '%(value)s с таким ИНН пользователя не существует',
                    params={'value': inn},
                )

        return data

    def clean_amount(self):
        data = self.cleaned_data['amount']
        if data < 0:
            raise ValidationError(
                '%(value)s сумма должна быть больше 0',
                params={'value': data},
            )
        return data

    def clean(self):
        data = self.cleaned_data
        required_keys = {'inn_to', 'user_from', 'amount'}

        if not (required_keys.issubset(set(data.keys()))):
            raise ValidationError(
                '%(value)s необходимы все поля',
                params={'value': data},
            )

        if data['user_from'].inn in self.list_inn_from_value(data['inn_to']):
            raise ValidationError(
                '%(value)s в списке находится ваш ИНН',
                params={'value': data['user_from'].inn},
            )

        if data['user_from'].balance < data['amount']:
            raise ValidationError(
                '%(value)s недостаточно денег %(amount)s',
                params={'value': data['user_from'].balance, 'amount': data['amount']},
            )

    def save(self):
        """
        В настройках установили ATOMIC_REQUESTS = True, что нам гарантирует фиксирование транзакций, при успешном
        выполнении запроса, иначе проиходит откат, поэтому все операции либо применятся, либо откатятся
        :return:
        """
        data = self.cleaned_data

        amount = data['amount']

        user_from = data['user_from']
        # так как прошла валидация то в amount у нас правильная сумма
        user_from.balance -= amount
        user_from.save()

        list_inn = self.list_inn_from_value(data['inn_to'])
        transfer_amount = amount / Decimal(len(list_inn))

        # чтобы не терять копеечки пользователя при делении округляем вниз
        # пример, 0.98/3  = 0.3266(6) а нам нужно 0.32
        transfer_amount.quantize(Decimal('0.01'), rounding=ROUND_DOWN)

        for inn in list_inn:
            user_to = get_user_model().objects.get(inn=inn)
            user_to.balance += transfer_amount
            user_to.save()

            transaction = Transaction()
            transaction.user_from = user_from
            transaction.user_to = user_to
            transaction.amount = transfer_amount
            transaction.save()

