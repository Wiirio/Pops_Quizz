# Generated by Django 3.0.6 on 2020-05-31 01:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quizz', '0012_auto_20200530_1029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='uuid',
            field=models.CharField(default='2E2486AC', editable=False, max_length=255, unique=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Quizz.Game'),
        ),
    ]