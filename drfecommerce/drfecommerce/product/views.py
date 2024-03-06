# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Category, Brand
from .serializers import CategorySerializer, ProductSerializer, BrandSerializer
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import action
from django.db.models import Prefetch
# from django.db import connection
# from sqlparse import format
# from pygments import highlight
# from pygments.formatters import TerminalFormatter
# from pygments.lexers import SqlLexer


class CategoryViewSet(viewsets.ViewSet):
    """A simple ViewSet - returning all categories in REST standard."""

    queryset = Category.objects.isactive()
    lookup_field = 'slug'

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)

        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """A simple ViewSet - returning all brands in REST standard."""

    queryset = Brand.objects.isactive()
    lookup_field = 'slug'

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)

        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """ViewSet for Product model."""

    queryset = Product.objects.isactive().prefetch_related(Prefetch('product_line__product_image'))
    lookup_field = 'slug'

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)

        return Response(serializer.data)

    @extend_schema(responses=ProductSerializer)
    @action(methods=['get'], detail=False, url_path=r'category/(?P<slug>[-\w]+)/all')
    def list_products_by_cat(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(category__slug=slug).select_related('brand', 'category'), many=True)
        x = Response(serializer.data)
        # for query in connection.queries:
        #     form = format(query['sql'], reindent=True)
        #     print(highlight(form, SqlLexer(), TerminalFormatter()))
        return x

    @extend_schema(responses=ProductSerializer)
    def retrieve(self, request, slug=None):
        serializer = ProductSerializer(
            self.queryset.filter(slug=slug).select_related('brand', 'category'), many=True)
        x = Response(serializer.data)
        # for query in connection.queries:
        #     form = format(query['sql'], reindent=True)
        #     print(highlight(form, SqlLexer(), TerminalFormatter()))
        return x
