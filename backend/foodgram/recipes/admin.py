from django.contrib import admin

from recipes import models
from foodgram import settings


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit', )
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'count', )
    search_fields = ('name',)
    list_filter = ('name', 'author', 'tags')
    empty_value_display = settings.EMPTY_VALUE_DISPLAY

    @admin.display(description='Число добавлений рецепта в избранное')
    def count(self, obj):
        return obj.favorites.count()


class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'color', 'slug', )
    search_fields = ('name', )
    list_filter = ('name', )
    empty_value_display = settings.EMPTY_VALUE_DISPLAY


class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ('ingredient', 'amount', )


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )


class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', )


admin.site.register(models.Ingredient, IngredientAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Tag, TagAdmin)
admin.site.register(models.RecipeIngredient, RecipeIngredientAdmin)
admin.site.register(models.Favorite, FavoriteAdmin)
admin.site.register(models.ShoppingCart, ShoppingCartAdmin)
