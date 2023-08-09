from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .models import Product, Category, Brand
from .serializers import CategorySerializer, ProductSerializer, BrandSerializer
from drf_spectacular.utils import extend_schema


class CategoryViewSet(viewsets.ViewSet):
    """A simple ViewSet - returning all categories in REST standard."""

    queryset = Category.objects.all()

    @extend_schema(responses=CategorySerializer)
    def list(self, request):
        serializer = CategorySerializer(self.queryset, many=True)

        return Response(serializer.data)


class BrandViewSet(viewsets.ViewSet):
    """A simple ViewSet - returning all brands in REST standard."""

    queryset = Brand.objects.all()

    @extend_schema(responses=BrandSerializer)
    def list(self, request):
        serializer = BrandSerializer(self.queryset, many=True)

        return Response(serializer.data)


class ProductViewSet(viewsets.ViewSet):
    """A simple ViewSet - returning all products in REST standard."""

    queryset = Product.objects.all()

    @extend_schema(responses=ProductSerializer)
    def list(self, request):
        serializer = ProductSerializer(self.queryset, many=True)

        return Response(serializer.data)
