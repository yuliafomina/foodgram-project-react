from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet, UserViewSet

app_name = 'api'


class NoPutRouter(DefaultRouter):
    """
    Router class that disables the PUT method.
    """
    def get_method_map(self, viewset, method_map):

        bound_methods = super().get_method_map(viewset, method_map)

        if 'put' in bound_methods.keys():
            del bound_methods['put']

        return bound_methods


router_v1 = NoPutRouter()

router_v1.register('ingredients', IngredientViewSet, basename='ingredients')
router_v1.register('tags', TagViewSet, basename='tags')
router_v1.register('recipes', RecipeViewSet, basename='recipes')
router_v1.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('', include(router_v1.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]
