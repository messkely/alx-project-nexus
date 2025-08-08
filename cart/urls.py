from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'carts', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')

urlpatterns = [
    # Cart management
    path('', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/', views.AddToCartView.as_view(), name='add_to_cart'),
    path('update/<int:item_id>/', views.UpdateCartItemView.as_view(), name='update_cart_item'),
    path('remove/<int:item_id>/', views.RemoveFromCartView.as_view(), name='remove_from_cart'),
    path('clear/', views.ClearCartView.as_view(), name='clear_cart'),
    path('count/', views.CartItemCountView.as_view(), name='cart_count'),
    path('total/', views.CartTotalView.as_view(), name='cart_total'),
    
    # Quick actions
    path('increase/<int:item_id>/', views.IncreaseQuantityView.as_view(), name='increase_quantity'),
    path('decrease/<int:item_id>/', views.DecreaseQuantityView.as_view(), name='decrease_quantity'),
    
    # ViewSet routes
    path('admin/', include(router.urls)),
]
