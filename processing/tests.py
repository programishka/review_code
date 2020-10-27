from decimal import Decimal

from django.apps import apps
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse

from processing.apps import ProcessingConfig
from processing.forms import TransferMoneyForm


class ExtensionUserTestCase(TestCase):
    def setUp(self):
        get_user_model().objects.create(
            inn="012345678901",
            username='u1',
            balance=Decimal('100'),
            first_name="u1",
            last_name="u1",
        )
        get_user_model().objects.create(
            inn="123456789012",
            username='u2',
            balance=Decimal('10'),
        )
        get_user_model().objects.create(
            inn="234567890123",
            username='u3',
            balance=Decimal('0'),
        )

    def test_form(self):
        # Пустая форма не валидна
        f = TransferMoneyForm()
        self.assertFalse(f.is_valid())

        # Больше чем на балансе
        u1 = get_user_model().objects.get(username='u1')
        data = {
            'user_from': u1,
            'inn_to': '123456789012',
            'amount': Decimal('10000'),
        }
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        # такого ИНН нет в базе
        data = {
            'user_from': u1,
            'inn_to': '210987654321',
            'amount': Decimal('1'),
        }
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        # короткий ИНН
        data.update({'inn_to': '210921'})
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        # недопустимые символы ИНН
        data.update({'inn_to': '123456e89012'})
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        #  нельзя переводить себе
        data.update({'inn_to': '012345678901'})
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        # отрицательная сумма
        data.update({'inn_to': '123456789012', 'amount': Decimal('-1')})
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        # Допустимо несколько ИНН, один недопустимый
        data = {
            'user_from': u1,
            'inn_to': '123456789012, 2345678q0123',
            'amount': Decimal('1'),
        }
        f = TransferMoneyForm(data)
        self.assertFalse(f.is_valid())

        # Допустимо несколько ИНН
        data = {
            'user_from': u1,
            'inn_to': '123456789012, 234567890123',
            'amount': Decimal('1'),
        }
        f = TransferMoneyForm(data)
        self.assertTrue(f.is_valid())

        # Сохраним
        f.save()

    def test_money_transfer_view(self):
        u1 = get_user_model().objects.get(username='u1')

        data = {
            'user_from': u1.pk,
            'inn_to': '123456789012, 234567890123',
            'amount': Decimal('1'),
        }
        c = Client()
        response = c.post(reverse('index'), data)

        # при успехе редирект
        self.assertEqual(response.status_code, 302)

        data = {
            'user_from': u1.pk,
            'inn_to': '123456789012, 234567890123',
            'amount': Decimal('1000'),
        }

        response = c.post(reverse('index'), data)
        # если ошибка 200
        self.assertEqual(response.status_code, 200)

    def test_apps(self):
        self.assertEqual(ProcessingConfig.name, 'processing')
        self.assertEqual(apps.get_app_config('processing').name, 'processing')

    def test_covered(self):
        pass
