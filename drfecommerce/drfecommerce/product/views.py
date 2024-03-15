# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Category, ProductLine, ProductImage
from .serializers import CategorySerializer, ProductSerializer, ProductCategorySerializer
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch
from django.db import connection
from sqlparse import format
from pygments import highlight
from pygments.formatters import TerminalFormatter
from pygments.lexers import SqlLexer


class CategoryViewSet(viewsets.ViewSet):
    """A simple ViewSet - returning all categories in REST standard."""

    queryset = Category.objects.is_active()
    lookup_field = 'slug'

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)

        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """ViewSet for Product model."""

    queryset = Product.objects.is_active()
    lookup_field = 'slug'

    @extend_schema(responses=ProductSerializer)
    @action(methods=['get'], detail=False, url_path=r'category/(?P<slug>[-\w]+)')
    def list_products_by_cat(self, request, slug=None):
        serializer = ProductCategorySerializer(
            self.queryset.filter(category__slug=slug)
            .prefetch_related(Prefetch('product_line', queryset=ProductLine.objects.is_active().order_by('order')))
            .prefetch_related(Prefetch('product_line__product_image', queryset=ProductImage.objects.filter(order=1)))
            , many=True)
        x = Response(serializer.data)
        # for query in connection.queries:
        #     form = format(query['sql'], reindent=True)
        #     print(highlight(form, SqlLexer(), TerminalFormatter()))
        return x

    @extend_schema(responses=ProductSerializer)
    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug)
            .prefetch_related(Prefetch('attribute_values__attribute'))
            .prefetch_related(Prefetch('product_line__product_image'))
            .prefetch_related(Prefetch('product_line__attribute_values__attribute'))
            , many=True)
        x = Response(serializer.data)
        queries = list(connection.queries)
        print(len(queries))
        # for query in queries:
        #     form = format(query['sql'], reindent=True)
        #     print(highlight(form, SqlLexer(), TerminalFormatter()))
        return x
