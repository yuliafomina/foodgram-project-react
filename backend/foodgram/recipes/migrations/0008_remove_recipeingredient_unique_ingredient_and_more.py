# Generated by Django 4.1 on 2022-08-24 14:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_remove_recipeingredient_unique_ingredient_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='recipeingredient',
            name='unique_ingredient',
        ),
        migrations.AddConstraint(
            model_name='recipeingredient',
            constraint=models.UniqueConstraint(fields=('ingredient', 'recipe'), name='unique_ingredient'),
        ),
    ]