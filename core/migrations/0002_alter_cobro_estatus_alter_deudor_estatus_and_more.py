# Generated by Django 4.0.4 on 2024-01-18 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cobro',
            name='estatus',
            field=models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Recibido')], default=0, verbose_name='Estatus'),
        ),
        migrations.AlterField(
            model_name='deudor',
            name='estatus',
            field=models.IntegerField(choices=[(0, 'Baja'), (1, 'Activo')], default=1, verbose_name='Estatus'),
        ),
        migrations.AlterField(
            model_name='deudor',
            name='mes_termina',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=2, verbose_name='Mes termina'),
        ),
        migrations.AlterField(
            model_name='pago',
            name='estatus',
            field=models.IntegerField(choices=[(0, 'Pendiente'), (1, 'Pagado'), (2, 'Cancelado')], default=0, verbose_name='Estatus'),
        ),
    ]
