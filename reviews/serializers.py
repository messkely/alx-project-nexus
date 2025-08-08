from rest_framework import serializers
from django.db.models import Avg
from .models import Review
from catalog.serializers import ProductSerializer
from users.models import User


class ReviewSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True)
    product_title = serializers.CharField(source='product.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'user', 'user_email', 'product', 'product_title', 
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class CreateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['product', 'rating', 'comment']

    def validate(self, attrs):
        user = self.context['request'].user
        product = attrs['product']
        
        # Check if user already reviewed this product
        if Review.objects.filter(user=user, product=product).exists():
            raise serializers.ValidationError("You have already reviewed this product.")
        
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UpdateReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value


class ProductReviewStatsSerializer(serializers.Serializer):
    total_reviews = serializers.IntegerField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2)
    rating_distribution = serializers.DictField()


class ReportReviewSerializer(serializers.Serializer):
    reason = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000, required=False)

    def validate_reason(self, value):
        allowed_reasons = [
            'inappropriate_content',
            'spam',
            'fake_review',
            'offensive_language',
            'other'
        ]
        if value not in allowed_reasons:
            raise serializers.ValidationError("Invalid reason.")
        return value
