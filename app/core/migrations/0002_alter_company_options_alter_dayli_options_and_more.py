# Generated by Django 4.2.1 on 2023-05-21 05:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'empresa', 'verbose_name_plural': 'empresas'},
        ),
        migrations.AlterModelOptions(
            name='dayli',
            options={'ordering': ('-id',), 'verbose_name': 'asistencia', 'verbose_name_plural': 'asistencias'},
        ),
        migrations.AddField(
            model_name='company',
            name='essalud',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='essalud %'),
        ),
        migrations.AddField(
            model_name='company',
            name='familiar_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True, verbose_name='asignación familiar s/.'),
        ),
        migrations.AddField(
            model_name='employ',
            name='cuspp',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AddField(
            model_name='employ',
            name='employ_type',
            field=models.CharField(default='OBRERO', max_length=50, verbose_name='Tipo de Trabajador'),
        ),
        migrations.AddField(
            model_name='employ',
            name='start_at',
            field=models.DateField(blank=True, null=True, verbose_name='Fec. Ingreso'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='afp_commision',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='afp_mandatory',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='afp_prima',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='created_at',
            field=models.DateField(auto_created=True, auto_now=True),
        ),
        migrations.AddField(
            model_name='invoice',
            name='essalud',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='familiar_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='h25_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='h35_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='hn_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='is_closed',
            field=models.BooleanField(default=False, verbose_name='bloqueado'),
        ),
        migrations.AddField(
            model_name='invoice',
            name='salary',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_income',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_income_company',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AddField(
            model_name='invoice',
            name='total_outcome',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=7),
        ),
        migrations.AlterField(
            model_name='dayli',
            name='h25_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='s/. horas al 25%'),
        ),
        migrations.AlterField(
            model_name='dayli',
            name='h35_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='s/. horas al 35%'),
        ),
        migrations.AlterField(
            model_name='dayli',
            name='hn_amount',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='s/. horas normales'),
        ),
        migrations.AlterField(
            model_name='dayli',
            name='total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='s/.'),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='days_lazy',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='invoice',
            name='days_worked',
            field=models.IntegerField(default=0),
        ),
        migrations.CreateModel(
            name='InvoiceDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=True, auto_now=True)),
                ('concept', models.CharField(max_length=50, verbose_name='concepto')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True, verbose_name='monto')),
                ('concept_type', models.IntegerField(choices=[(1, 'Ingresos'), (2, 'Descuentos'), (3, 'Aportaciones')])),
                ('invoice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.invoice')),
            ],
        ),
    ]
