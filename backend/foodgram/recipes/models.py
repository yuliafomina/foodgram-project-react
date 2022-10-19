from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.functions import Upper


class Ingredient(models.Model):
    name = models.CharField(
        'Название ингредиента',
        max_length=200)
    measurement_unit = models.CharField(
        'Единица измерения',
        max_length=20)

    class Meta:
        ordering = [Upper('name'), ]
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Tag(models.Model):
    name = models.CharField(
        'Тег',
        max_length=50,
        unique=True)
    color = models.CharField(
        'Цвет в формате HEX',
        max_length=16,
        unique=True)
    slug = models.SlugField(
        'Slug',
        max_length=100,
        unique=True)

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор')
    name = models.CharField(
        'Название',
        max_length=200)
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes')
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='static/recipes/')
    text = models.TextField(
        'Способ приготовления')
    cooking_time = models.PositiveIntegerField(
        'Время приготовления',
        validators=[MinValueValidator(1)],
        help_text='Время приготовления должно быть больше 1 минуты',
    )
    pub_date = models.DateTimeField(
        'Дата публикации',
        auto_now_add=True)

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент',
        related_name='ingredient'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='recipes'
    )
    amount = models.IntegerField(
        validators=[MinValueValidator(1)],
        help_text='Количество ингредиентов должно быть больше единицы',
        verbose_name='Количество ингредиентов'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields={'recipe', 'ingredient'},
                name='unique_ingredient'
            ),
        ]
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецептов'


class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='favorites'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite',
            ),
        ]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        ordering = ('user',)

    def __str__(self):
        return f'{self.user.username} {self.recipe}'


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Пользователь',
        related_name='carts'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        verbose_name='Рецепт',
        related_name='carts'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_shopping_cart',
            ),
        ]
        verbose_name = 'Cписок покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'{self.user.username} {self.recipe}'
