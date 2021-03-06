# Generated by Django 3.0.4 on 2020-05-12 21:49

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0012_auto_20200508_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='incident',
            name='date',
            field=models.DateField(default=datetime.datetime(2020, 5, 13, 0, 49, 38, 563733), verbose_name='Ημερομηνία Καταχώρησης'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='time',
            field=models.TimeField(default=datetime.datetime(2020, 5, 13, 0, 49, 38, 563733), verbose_name='Ώρα Καταχώρησης'),
        ),
        migrations.AlterField(
            model_name='incident',
            name='user_username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporter.User_Res', verbose_name='Όνομα Χρήστη'),
        ),
        migrations.AlterField(
            model_name='problems',
            name='picture',
            field=models.ImageField(blank=True, upload_to='media', verbose_name='picture'),
        ),
        migrations.AlterField(
            model_name='user_res',
            name='visit_time',
            field=models.DateField(blank=True, null=True, verbose_name='Ημερομηνία Αναχώρησης'),
        ),
    ]
