# Generated by Django 4.2.1 on 2023-05-31 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_dayli_is_closed'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afponp',
            name='is_onp',
            field=models.BooleanField(default=False, verbose_name='es onp'),
        ),
    ]
