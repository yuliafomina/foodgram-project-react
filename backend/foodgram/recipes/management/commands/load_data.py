import csv
import os

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Команда для загрузки ингредиентов'

    def handle(self, *args, **options):
        self.stdout.write('Загрузка...')

        file_path = os.path.join(
            os.path.abspath(os.path.dirname('manage.py')),
            r'C:\Dev\foodgram-project-react\data\ingredients.csv',
        )

        with open(file_path, encoding='utf8') as csvfile:
            reader = csv.DictReader(
                csvfile, fieldnames=['name', 'measurement_unit']
            )
            for row in reader:
                Ingredient.objects.update_or_create(**row)

        self.stdout.write(self.style.SUCCESS('Ингредиенты загружены'))
