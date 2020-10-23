"""Весь процессин выносим в это приложение"""

from django.contrib.auth import get_user_model
from django.db import models


class Transaction(models.Model):
    """
    Все пользователи хотят видеть историю транзакций
    """

    user_from = models.ForeignKey(
        get_user_model(),
        verbose_name="Отправитель", on_delete=models.PROTECT, related_name="transaction_from_user"
    )
    user_to = models.ForeignKey(
        get_user_model(),
        verbose_name="Получатель", on_delete=models.PROTECT, related_name="transaction_to_user"
    )

    # для сумм используем DecimalField, так как работаем с денежками и погрешности нам не нужны
    amount = models.DecimalField(verbose_name="Сумма", max_digits=18, decimal_places=2)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
