# Generated by Django 3.2.23 on 2024-01-10 22:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('walls', '0001_initial'),
        ('wallitems', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='wallitem',
            name='wall',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='walls.wall'),
        ),
    ]