# Generated by Django 4.1.2 on 2022-10-20 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shortener", "0003_alter_shortener_redirect_link"),
    ]

    operations = [
        migrations.AlterField(
            model_name="shortener",
            name="redirect_link",
            field=models.CharField(blank=True, max_length=255, unique=True),
        ),
    ]