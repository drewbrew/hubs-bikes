# Generated by Django 3.1.5 on 2021-01-28 16:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0002_auto_20171227_2246"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="first_name",
            field=models.CharField(
                blank=True, max_length=150, verbose_name="first name"
            ),
        ),
    ]
