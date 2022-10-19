import io
import os

from django.conf import settings

from api.filters import IngredientFilter, RecipeFilter
from api.permissions import IsOwnerAdminOrReadOnly
from django.db.models import Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from recipes.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                            ShoppingCart, Tag)
from reportlab.lib.units import inch
from reportlab.lib import pagesizes
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.rl_config import defaultPageSize
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from rest_framework import permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from users.models import Follow, User

from . import serializers, paginators


class IngredientViewSet(ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = serializers.IngredientSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilter


class TagViewSet(ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer
    pagination_class = None


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = serializers.RecipeSerializer
    permission_classes = (IsOwnerAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    pagination_class = paginators.LimitPaginator

    def get_serializer_class(self):
        if self.request.method in permissions.SAFE_METHODS:
            return serializers.GetRecipeSerializer
        return serializers.RecipeSerializer

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if Favorite.objects.filter(
                    recipe=recipe, user=self.request.user
            ).exists():
                return Response(
                    'Рецепт уже в избранном!',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Favorite.objects.create(recipe=recipe, user=self.request.user)
            serializer = serializers.RecipePreviewSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        favorited = Favorite.objects.filter(
            recipe=recipe, user_id=self.request.user
        )
        if favorited.exists():
            favorited.delete()
            return Response(
                'Рецепт удален из любимых!', status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Ошибка запроса!', status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    recipe=recipe, user=self.request.user
            ).exists():
                return Response(
                    'Рецепт уже в cписке покупок!',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            ShoppingCart.objects.create(recipe=recipe, user=self.request.user)
            serializer = serializers.RecipePreviewSerializer(
                recipe, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        in_shopping_cart = ShoppingCart.objects.filter(
            recipe=recipe, user_id=self.request.user
        )
        if in_shopping_cart.exists():
            in_shopping_cart.delete()
            return Response(
                'Рецепт удален из списка!', status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Ошибка запроса!', status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
        )
    def download_shopping_cart(self, request):
        def firstPageContent(page_canvas, document):
            header_content = 'Список покупок'
            headerHeight = defaultPageSize[1] - 50
            headerWidth = defaultPageSize[0]/2.0

            page_canvas.saveState()
            page_canvas.setFont('Verdana', 18)
            page_canvas.drawCentredString(
                headerWidth,
                headerHeight,
                header_content
            )
            page_canvas.restoreState()

        pdfmetrics.registerFont(
            TTFont('Verdana', os.path.join(settings.FONTS_ROOT, 'Verdana.ttf'))
        )

        shopping_cart = RecipeIngredient.objects.filter(
            recipe__carts__user=request.user
        ).values(
            'ingredient__name', 'ingredient__measurement_unit'
        ).annotate(
            ingredient_amount=Sum('amount')
        ).values_list(
            'ingredient__name',
            'ingredient_amount',
            'ingredient__measurement_unit'
        )

        document_content = [
            (ingredient[0], ingredient[1], ingredient[2])
            for ingredient in shopping_cart
        ]

        buffer = io.BytesIO()
        document = SimpleDocTemplate(
            buffer,
            pagesize=pagesizes.portrait(pagesizes.A4),
        )

        columns_width = [6*inch, 1*inch, 1*inch]
        table = Table(
            document_content,
            rowHeights=20,
            repeatRows=1,
            colWidths=columns_width,
            hAlign='CENTER'
        )

        table.setStyle(TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 18),
            ('FONTNAME', (0, 0), (-1, -1), "Verdana"),
        ]))

        document.build([table], onFirstPage=firstPageContent)

        buffer.seek(0)
        return FileResponse(
            buffer, as_attachment=True, filename='shopping_cart.pdf',
        )


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    pagination_class = paginators.LimitPaginator

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        serializer = self.get_serializer(user)
        return Response(serializer.data)

    @action(
        methods=['post'],
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def set_password(self, request):
        user = self.request.user
        serializer = serializers.PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response(
                'Пароль установлен!', status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Ошибка', status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        methods=['post', 'delete'],
        detail=True,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscribe(self, request, pk):
        author = get_object_or_404(User, id=pk)
        if request.method == 'POST':
            if self.request.user == author:
                return Response(
                    'Подписка на себя запрещена!',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            if Follow.objects.filter(
                    author=author, user=self.request.user
            ).exists():
                return Response(
                    'Вы уже подписаны!',
                    status=status.HTTP_400_BAD_REQUEST,
                )
            Follow.objects.create(author=author, user=self.request.user)
            serializer = serializers.FollowSerializer(
                author, context={'request': request}
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        subscription = Follow.objects.filter(
            author=author, user_id=self.request.user
        )
        if subscription.exists():
            subscription.delete()
            return Response(
                'Подписка отменена!', status=status.HTTP_204_NO_CONTENT
            )
        return Response(
            'Подписка не существует!', status=status.HTTP_400_BAD_REQUEST
        )

    @action(
        detail=False,
        permission_classes=(permissions.IsAuthenticated,)
    )
    def subscriptions(self, request):
        user = self.request.user
        queryset = User.objects.filter(following__user=user).all()
        results = self.paginate_queryset(queryset)
        serializer = serializers.FollowSerializer(
            results, context={"request": request}, many=True
        )
        return self.get_paginated_response(serializer.data)
