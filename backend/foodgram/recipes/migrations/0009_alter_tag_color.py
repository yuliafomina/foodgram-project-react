# Generated by Django 4.1 on 2022-08-31 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_remove_recipeingredient_unique_ingredient_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=16, unique=True, verbose_name='Цвет в формате HEX'),
        ),
    ]
