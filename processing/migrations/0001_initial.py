# Generated by Django 3.1.2 on 2020-10-23 19:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=18, verbose_name='Сумма')),
                ('user_from', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transaction_from_user', to=settings.AUTH_USER_MODEL, verbose_name='Отправитель')),
                ('user_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transaction_to_user', to=settings.AUTH_USER_MODEL, verbose_name='Получатель')),
            ],
            options={
                'verbose_name': 'Транзакция',
                'verbose_name_plural': 'Транзакции',
            },
        ),
    ]