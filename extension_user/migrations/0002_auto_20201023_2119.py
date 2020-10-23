# Generated by Django 3.1.2 on 2020-10-23 21:19

from django.db import migrations, models
import extension_user.models


class Migration(migrations.Migration):

    dependencies = [
        ('extension_user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extensionuser',
            name='inn',
            field=models.CharField(db_index=True, max_length=12, unique=True, validators=[extension_user.models.validate_inn], verbose_name='ИНН'),
        ),
    ]
