from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for admin endpoints with disabled root view
admin_router = DefaultRouter(trailing_slash=False)
admin_router.include_root_view = False  # Disable the automatic API root
admin_router.register('products', views.ProductViewSet, basename='admin-product')
admin_router.register('categories', views.CategoryViewSet, basename='admin-category')

urlpatterns = [
    # Specific product endpoints (must come before router patterns)
    path('products/search/', views.ProductSearchView.as_view(), name='product_search'),
    path('products/featured/', views.FeaturedProductsView.as_view(), name='featured_products'),
    path('products/latest/', views.LatestProductsView.as_view(), name='latest_products'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('products/<slug:slug>/', views.ProductBySlugView.as_view(), name='product_by_slug'),
    
    # Specific category endpoints (must come before router patterns)
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('categories/<slug:slug>/', views.CategoryBySlugView.as_view(), name='category_by_slug'),
    path('categories/<int:pk>/products/', views.CategoryProductsView.as_view(), name='category_products'),
    
    # Admin endpoints - include router but disable root view, add custom secured root
    path('admin/', include([
        path('', views.admin_root, name='admin_root'),  # Custom admin root view
        path('', include(admin_router.urls)),  # ViewSet endpoints
    ])),
]
