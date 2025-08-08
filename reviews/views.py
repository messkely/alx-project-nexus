from django.shortcuts import get_object_or_404
from django.db.models import Avg, Count
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .models import Review
from .serializers import (
    ReviewSerializer,
    CreateReviewSerializer,
    UpdateReviewSerializer,
    ProductReviewStatsSerializer,
    ReportReviewSerializer
)
from catalog.models import Product
from users.models import User


class ReviewListView(generics.ListAPIView):
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CreateReviewView(generics.CreateAPIView):
    serializer_class = CreateReviewSerializer
    permission_classes = [IsAuthenticated]


class ReviewDetailView(generics.RetrieveAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class UpdateReviewView(generics.UpdateAPIView):
    serializer_class = UpdateReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(user=self.request.user)


class DeleteReviewView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(user=self.request.user)


class ProductReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        product_id = self.kwargs['product_id']
        return Review.objects.filter(product_id=product_id).order_by('-created_at')


class ProductReviewStatsView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, product_id):
        product = get_object_or_404(Product, id=product_id)
        reviews = Review.objects.filter(product=product)
        
        if not reviews.exists():
            return Response({
                'total_reviews': 0,
                'average_rating': 0,
                'rating_distribution': {str(i): 0 for i in range(1, 6)}
            })
        
        total_reviews = reviews.count()
        average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
        
        # Calculate rating distribution
        rating_distribution = {}
        for i in range(1, 6):
            count = reviews.filter(rating=i).count()
            rating_distribution[str(i)] = count
        
        data = {
            'total_reviews': total_reviews,
            'average_rating': round(average_rating, 2) if average_rating else 0,
            'rating_distribution': rating_distribution
        }
        
        return Response(data)


class UserReviewsView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(user=self.request.user).order_by('-created_at')


class UserReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Review.objects.filter(user_id=user_id).order_by('-created_at')


class MarkReviewHelpfulView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        
        # In a real app, you'd want to track which users found reviews helpful
        # For now, just return a success message
        return Response({
            'message': 'Review marked as helpful.',
            'review_id': review.id
        })


class ReportReviewView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        review = get_object_or_404(Review, pk=pk)
        serializer = ReportReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            # In a real app, you'd save the report to a database
            # For now, just return a success message
            return Response({
                'message': 'Review reported successfully.',
                'review_id': review.id,
                'reason': serializer.validated_data['reason']
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
