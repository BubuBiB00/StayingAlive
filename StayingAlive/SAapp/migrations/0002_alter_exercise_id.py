# Generated by Django 4.2.6 on 2024-02-16 08:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SAapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='exercise',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
