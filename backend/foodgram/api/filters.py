from django_filters import rest_framework as filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(filters.FilterSet):
    """Recipes filtering by tags, author, favorite, shopping cart."""

    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )
    is_favorited = filters.BooleanFilter(
        method='get_boolean',
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='get_boolean',
    )

    def get_boolean(self, queryset, name, value):
        if value:
            if name == 'is_favorited':
                queryset = queryset.filter(
                    favorites__user=self.request.user
                )
            if name == 'is_in_shopping_cart':
                queryset = queryset.filter(
                    carts__user=self.request.user
                )
        return queryset

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')


class IngredientFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)
