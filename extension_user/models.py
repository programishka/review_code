from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models


def validate_inn(value):
    try:
        int(value)
    except ValueError:
        raise ValidationError(
            '%(value)s значение ИНН должно содержать только цифры',
            params={'value': value},
        )

    if len(value) != 12:
        raise ValidationError(
            '%(value)s ИНН состоять из 12 цифр',
            params={'value': value},
        )


class ExtensionUser(AbstractUser):
    """
    Мы можем спокойно расширять модель пользователя
    """

    REQUIRED_FIELDS = ['email', 'inn']

    # Так как в ИНН может встречаться лидирующие нули будем хранить в виде строки,
    inn = models.CharField(
        verbose_name="ИНН", max_length=12, unique=True, blank=False, null=False,
        db_index=True, validators=[validate_inn]
    )
    balance = models.DecimalField(verbose_name="Баланс", default=0, max_digits=18, decimal_places=2)

    def __str__(self):
        return f'{self.inn}  {self.first_name} {self.last_name} = {self.balance}'

    def save(self, *args, **kwargs):
        validate_inn(self.inn)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
