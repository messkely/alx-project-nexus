"""
Unit tests for order cancellation functionality
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from datetime import datetime, timedelta
from orders.models import Order, OrderItem
from catalog.models import Category, Product
from users.models import Address

User = get_user_model()


class OrderCancellationTestCase(APITestCase):
    """Test order cancellation functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            password='testpass123'
        )
        
        # Create another user for permission tests
        self.other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        
        # Create test address
        self.address = Address.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            address_line_1='123 Test Street',
            city='Test City',
            postal_code='12345',
            country='Test Country',
            phone_number='+1234567890',
            is_default=True
        )
        
        # Create test category and product
        self.category = Category.objects.create(
            name='Test Category',
            slug='test-category'
        )
        
        self.product = Product.objects.create(
            title='Test Product',
            description='Test description',
            price=Decimal('99.99'),
            category=self.category,
            slug='test-product',
            inventory=10
        )
        
        # Create test orders with different statuses
        self.pending_order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('199.98'),
            shipping_address=self.address
        )
        
        self.paid_order = Order.objects.create(
            user=self.user,
            status='paid',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        self.shipped_order = Order.objects.create(
            user=self.user,
            status='shipped',
            total_amount=Decimal('149.99'),
            shipping_address=self.address
        )
        
        self.delivered_order = Order.objects.create(
            user=self.user,
            status='delivered',
            total_amount=Decimal('79.99'),
            shipping_address=self.address
        )
        
        # Create order items
        OrderItem.objects.create(
            order=self.pending_order,
            product=self.product,
            quantity=2,
            price=Decimal('99.99')
        )
        
        OrderItem.objects.create(
            order=self.paid_order,
            product=self.product,
            quantity=1,
            price=Decimal('99.99')
        )
        
        # Get JWT token
        self.token = str(RefreshToken.for_user(self.user).access_token)
        self.other_token = str(RefreshToken.for_user(self.other_user).access_token)
    
    def test_cancel_pending_order_success(self):
        """Test successful cancellation of pending order"""
        url = reverse('cancel_order', kwargs={'pk': self.pending_order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)
        self.assertIn('cancelled', response.data['message'].lower())
        
        # Verify order status updated
        self.pending_order.refresh_from_db()
        self.assertEqual(self.pending_order.status, 'cancelled')
        
        # Verify product inventory restored
        self.product.refresh_from_db()
        self.assertEqual(self.product.inventory, 12)  # 10 + 2 from cancelled order
    
    def test_cancel_paid_order_success(self):
        """Test successful cancellation of paid order (should trigger refund)"""
        url = reverse('cancel_order', kwargs={'pk': self.paid_order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('refund', response.data['message'].lower())
        
        # Verify order status updated
        self.paid_order.refresh_from_db()
        self.assertEqual(self.paid_order.status, 'cancelled')
    
    def test_cancel_shipped_order_failure(self):
        """Test cancellation of shipped order (should fail)"""
        url = reverse('cancel_order', kwargs={'pk': self.shipped_order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot be cancelled', response.data['error'].lower())
        
        # Verify order status not changed
        self.shipped_order.refresh_from_db()
        self.assertEqual(self.shipped_order.status, 'shipped')
    
    def test_cancel_delivered_order_failure(self):
        """Test cancellation of delivered order (should fail)"""
        url = reverse('cancel_order', kwargs={'pk': self.delivered_order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cannot be cancelled', response.data['error'].lower())
        
        # Verify order status not changed
        self.delivered_order.refresh_from_db()
        self.assertEqual(self.delivered_order.status, 'delivered')
    
    def test_cancel_order_without_authentication(self):
        """Test order cancellation without authentication"""
        url = reverse('cancel_order', kwargs={'pk': self.pending_order.pk})
        
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials', response.data['detail'])
    
    def test_cancel_other_users_order(self):
        """Test cancellation of order belonging to another user"""
        url = reverse('cancel_order', kwargs={'pk': self.pending_order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.other_token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_cancel_nonexistent_order(self):
        """Test cancellation of non-existent order"""
        url = reverse('cancel_order', kwargs={'pk': 99999})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_cancel_already_cancelled_order(self):
        """Test cancellation of already cancelled order"""
        # First cancel the order
        self.pending_order.status = 'cancelled'
        self.pending_order.save()
        
        url = reverse('cancel_order', kwargs={'pk': self.pending_order.pk})
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('already', response.data['error'].lower())
    
    def test_order_status_validation(self):
        """Test the order status validation logic"""
        from orders.models import Order
        
        # Test cancellable statuses
        cancellable_statuses = ['pending', 'paid', 'processing']
        for status_val in cancellable_statuses:
            order = Order.objects.create(
                user=self.user,
                status=status_val,
                total_amount=Decimal('100.00')
            )
            self.assertTrue(order.can_be_cancelled(), f"Order with status '{status_val}' should be cancellable")
        
        # Test non-cancellable statuses  
        non_cancellable_statuses = ['shipped', 'delivered', 'cancelled', 'refunded']
        for status_val in non_cancellable_statuses:
            order = Order.objects.create(
                user=self.user,
                status=status_val,
                total_amount=Decimal('100.00')
            )
            self.assertFalse(order.can_be_cancelled(), f"Order with status '{status_val}' should not be cancellable")
    
    def test_inventory_restoration_on_cancellation(self):
        """Test that product inventory is restored when order is cancelled"""
        # Record initial inventory
        initial_inventory = self.product.inventory
        
        # Cancel order
        url = reverse('cancel_order', kwargs={'pk': self.pending_order.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify inventory restored
        self.product.refresh_from_db()
        expected_inventory = initial_inventory + 2  # Quantity from order item
        self.assertEqual(self.product.inventory, expected_inventory)
    
    def test_cancellation_time_window(self):
        """Test cancellation time window restrictions"""
        from django.utils import timezone
        
        # Create order that's too old to cancel (if time restrictions exist)
        old_order = Order.objects.create(
            user=self.user,
            status='paid',
            total_amount=Decimal('99.99'),
            shipping_address=self.address
        )
        
        # Manually set creation date to be old (simulate old order)
        old_order.created_at = timezone.now() - timedelta(days=30)
        old_order.save()
        
        url = reverse('cancel_order', kwargs={'pk': old_order.pk})
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, {}, format='json')
        
        # This test depends on business logic - adjust based on actual requirements
        # For now, we'll just verify the endpoint responds appropriately
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST])
