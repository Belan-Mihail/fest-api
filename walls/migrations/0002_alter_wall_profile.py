# Generated by Django 3.2.23 on 2024-01-11 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('walls', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wall',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='profiles.profile'),
        ),
    ]