# Generated by Django 5.1.2 on 2024-11-28 19:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='stock',
            field=models.PositiveIntegerField(default=0),
        ),
    ]