# Generated by Django 4.2.1 on 2023-05-23 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_company_options_alter_dayli_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='dayli',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='bloqueado'),
        ),
    ]