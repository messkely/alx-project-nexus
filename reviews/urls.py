from django.urls import path
from . import views

urlpatterns = [
    # Review management
    path('', views.ReviewListView.as_view(), name='review_list'),
    path('create/', views.CreateReviewView.as_view(), name='create_review'),
    path('<int:pk>/', views.ReviewDetailView.as_view(), name='review_detail'),
    path('<int:pk>/update/', views.UpdateReviewView.as_view(), name='update_review'),
    path('<int:pk>/delete/', views.DeleteReviewView.as_view(), name='delete_review'),
    
    # Product reviews
    path('product/<int:product_id>/', views.ProductReviewsView.as_view(), name='product_reviews'),
    path('product/<int:product_id>/stats/', views.ProductReviewStatsView.as_view(), name='product_review_stats'),
    
    # User reviews
    path('user/', views.UserReviewsView.as_view(), name='user_reviews'),
    path('user/<int:user_id>/', views.UserReviewListView.as_view(), name='user_review_list'),
    
    # Review actions
    path('<int:pk>/helpful/', views.MarkReviewHelpfulView.as_view(), name='mark_helpful'),
    path('<int:pk>/report/', views.ReportReviewView.as_view(), name='report_review'),
]
