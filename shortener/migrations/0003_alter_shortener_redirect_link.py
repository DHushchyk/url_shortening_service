# Generated by Django 4.1.2 on 2022-10-20 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0002_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortener",
            name="redirect_link",
            field=models.CharField(blank=True, max_length=38, unique=True),
        ),
    ]
