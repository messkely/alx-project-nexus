from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
# ViewSets can be added here if needed later

urlpatterns = [
    # Order management
    path('', views.OrderListView.as_view(), name='order_list'),
    path('create/', views.CreateOrderView.as_view(), name='create_order'),
    path('<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
    path('<int:pk>/cancel/', views.CancelOrderView.as_view(), name='cancel_order'),
    path('<int:pk>/status/', views.OrderStatusView.as_view(), name='order_status'),
    
    # Order tracking
    path('<int:pk>/track/', views.TrackOrderView.as_view(), name='track_order'),
    path('history/', views.OrderHistoryView.as_view(), name='order_history'),
    
    # Payment
    path('<int:pk>/payment/', views.ProcessPaymentView.as_view(), name='process_payment'),
    path('<int:pk>/payment/confirm/', views.ConfirmPaymentView.as_view(), name='confirm_payment'),
    
    # Admin endpoints
    path('admin/all/', views.AdminOrderListView.as_view(), name='admin_order_list'),
    path('admin/<int:pk>/update-status/', views.UpdateOrderStatusView.as_view(), name='update_order_status'),
]
