# Generated by Django 4.1.3 on 2022-11-20 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booking', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='status',
            field=models.CharField(choices=[('OPEN', 'Open'), ('RESERVED', 'Reserved'), ('FINISHED', 'Finishd'), ('CANCELED', 'Canceled')], default='OPEN', max_length=20),
        ),
    ]