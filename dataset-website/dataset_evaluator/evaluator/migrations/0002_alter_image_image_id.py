# Generated by Django 4.2.2 on 2023-11-28 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("evaluator", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="image",
            name="image_id",
            field=models.CharField(max_length=16),
        ),
    ]