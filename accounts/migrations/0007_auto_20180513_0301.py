# Generated by Django 2.0.2 on 2018-05-13 01:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_change'),
    ]

    operations = [
        migrations.AlterField(
            model_name='change',
            name='note',
            field=models.CharField(blank=True, default=' ', max_length=200),
        ),
    ]