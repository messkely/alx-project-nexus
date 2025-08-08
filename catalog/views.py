from rest_framework import viewsets, filters, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from .models import Product, Category
from .serializers import ProductSerializer, CategorySerializer
from .permissions import IsAdminOrReadOnly, IsAuthenticatedAdmin


@api_view(['GET'])
@permission_classes([IsAuthenticatedAdmin])
def admin_root(request, format=None):
    """
    Admin-only API root view.
    Only authenticated staff users can access this endpoint to see available admin operations.
    """
    return Response({
        'products': reverse('admin-product-list', request=request, format=format),
        'categories': reverse('admin-category-list', request=request, format=format),
    })


class ProductViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for managing products.
    Requires authentication and staff privileges for all operations.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedAdmin]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['category', 'price']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['created_at']


class CategoryViewSet(viewsets.ModelViewSet):
    """
    Admin-only ViewSet for managing categories.
    Requires authentication and staff privileges for all operations.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedAdmin]


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ['category', 'price']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['created_at']


class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductBySlugView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class ProductSearchView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        if query:
            return Product.objects.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )
        return Product.objects.none()


class FeaturedProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_queryset(self):
        # Assuming we'll add a 'featured' field to Product model later
        # For now, return products ordered by creation date
        return Product.objects.all().order_by('-created_at')[:10]


class LatestProductsView(generics.ListAPIView):
    queryset = Product.objects.all().order_by('-created_at')[:20]
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryDetailView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryBySlugView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'


class CategoryProductsView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    ordering_fields = ['price', 'created_at', 'title']
    ordering = ['created_at']
    
    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Product.objects.none()
        category_id = self.kwargs['pk']
        return Product.objects.filter(category_id=category_id)
