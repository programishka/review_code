from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase
from django.apps import apps


from extension_user.apps import ExtensionUserConfig


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

    def test_validate_inn(self):
        u = get_user_model()()
        u.username = "u15"
        u.first_name = "u15"
        u.last_name = "u15"
        u.balance = Decimal('0.0')

        # Нормальное сохранение
        u.inn = "789012345678"
        u.save()

        # Короткий ИНН
        u.inn = "111"
        with self.assertRaises(ValidationError):
            u.save()

        # Не допустимые символы
        u.inn = "1234е6789012"
        with self.assertRaises(ValidationError):
            u.save()

        # Длинный ИНН
        u.inn = "1234567890123456"
        with self.assertRaises(ValidationError):
            u.save()

        # Дубликат ИНН
        u.inn = "123456789012"
        with self.assertRaises(IntegrityError):
            u.save()

    def test_balance(self):
        # Потеря точности

        a = 0.1 + 0.1 + 0.1
        self.assertNotEqual(a, 0.3)

        b = Decimal('0.1') + Decimal('0.1') + Decimal('0.1')
        self.assertEqual(b, Decimal('0.3'))

        u = get_user_model()()
        u.username = "u16"
        u.first_name = "u16"
        u.last_name = "u16"
        u.balance = b
        u.inn = "789012345678"
        u.save()

        u = get_user_model().objects.get(username="u16")
        self.assertEqual(u.balance, Decimal('0.3'))

        u.balance = a
        u.save()
        u = get_user_model().objects.get(username="u16")

        self.assertNotEqual(u.balance, 0.3)
        self.assertEqual(u.balance, Decimal('0.3'))

    def test_presentation(self):
        u1 = get_user_model().objects.get(username='u1')
        self.assertEqual(str(u1), '012345678901  u1 u1 = 100.00')

    def test_apps(self):
        self.assertEqual(ExtensionUserConfig.name, 'extension_user')
        self.assertEqual(apps.get_app_config('extension_user').name, 'extension_user')

    def test_covered(self):
        pass
