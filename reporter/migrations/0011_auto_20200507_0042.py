# Generated by Django 3.0.4 on 2020-05-06 21:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reporter', '0010_auto_20200507_0015'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='incident',
            options={'verbose_name_plural': 'Incidents'},
        ),
        migrations.RenameField(
            model_name='incident',
            old_name='user_email',
            new_name='user_username',
        ),
        migrations.AlterField(
            model_name='incident',
            name='problem_kind',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reporter.Problems'),
        ),
    ]
