from rest_framework import serializers
from django.db.models import Avg
from .models import Product, Category


class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'products_count']

    def get_products_count(self, obj):
        return obj.products.count()


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    average_rating = serializers.SerializerMethodField()
    reviews_count = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'slug', 'description', 'price', 'category', 
            'category_name', 'image', 'stock_quantity', 'created_at', 
            'updated_at', 'average_rating', 'reviews_count'
        ]

    def get_average_rating(self, obj):
        avg_rating = obj.reviews.aggregate(Avg('rating'))['rating__avg']
        return round(avg_rating, 2) if avg_rating else 0

    def get_reviews_count(self, obj):
        return obj.reviews.count()


class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'description', 'price', 'category', 'image', 'stock_quantity']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock quantity cannot be negative.")
        return value
