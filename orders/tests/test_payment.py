"""
Unit tests for payment functionality
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from decimal import Decimal
from unittest.mock import patch, MagicMock
from orders.models import Order, OrderItem
from catalog.models import Category, Product
from users.models import Address

User = get_user_model()


class PaymentEndpointTestCase(APITestCase):
    """Test payment endpoint functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = APIClient()
        
        # Create test user
        self.user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
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
        
        # Create test order
        self.order = Order.objects.create(
            user=self.user,
            status='pending',
            total_amount=Decimal('199.98'),
            shipping_address=self.address
        )
        
        # Create order items
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2,
            price=Decimal('99.99')
        )
        
        # Get JWT token
        self.token = str(RefreshToken.for_user(self.user).access_token)
    
    def test_payment_without_authentication(self):
        """Test payment endpoint without authentication"""
        url = reverse('payment_complete', kwargs={'pk': self.order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': str(self.order.total_amount)
        }
        
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('Authentication credentials', response.data['detail'])
    
    @patch('orders.views.process_payment')
    def test_payment_with_valid_data(self, mock_process_payment):
        """Test payment endpoint with valid payment data"""
        # Mock successful payment processing
        mock_process_payment.return_value = {
            'success': True,
            'transaction_id': 'txn_123456789',
            'amount': self.order.total_amount,
            'status': 'completed'
        }
        
        url = reverse('payment_complete', kwargs={'pk': self.order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': str(self.order.total_amount)
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('payment_successful', response.data)
        self.assertTrue(response.data['payment_successful'])
        
        # Verify order status updated
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'paid')
    
    def test_payment_with_invalid_card_number(self):
        """Test payment with invalid card number"""
        url = reverse('payment_complete', kwargs={'pk': self.order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '1234',  # Invalid card number
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': str(self.order.total_amount)
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('card_number', response.data)
    
    def test_payment_with_expired_card(self):
        """Test payment with expired card"""
        url = reverse('payment_complete', kwargs={'pk': self.order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '01',  # Past date
            'expiry_year': '2020',
            'cvv': '123',
            'amount': str(self.order.total_amount)
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('expired', str(response.data).lower())
    
    def test_payment_with_mismatched_amount(self):
        """Test payment with amount that doesn't match order total"""
        url = reverse('payment_complete', kwargs={'pk': self.order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': '100.00'  # Different from order total
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', str(response.data).lower())
    
    def test_payment_for_nonexistent_order(self):
        """Test payment for non-existent order"""
        url = reverse('payment_complete', kwargs={'pk': 99999})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': '199.98'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_payment_for_other_users_order(self):
        """Test payment for order belonging to another user"""
        # Create another user and order
        other_user = User.objects.create_user(
            email='other@example.com',
            username='otheruser',
            password='testpass123'
        )
        
        other_order = Order.objects.create(
            user=other_user,
            status='pending',
            total_amount=Decimal('99.99')
        )
        
        url = reverse('payment_complete', kwargs={'pk': other_order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': '99.99'
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    @patch('orders.views.process_payment')
    def test_payment_processing_failure(self, mock_process_payment):
        """Test payment when payment processing fails"""
        # Mock failed payment processing
        mock_process_payment.return_value = {
            'success': False,
            'error': 'Payment declined by bank',
            'error_code': 'DECLINED'
        }
        
        url = reverse('payment_complete', kwargs={'pk': self.order.pk})
        payment_data = {
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': '2025',
            'cvv': '123',
            'amount': str(self.order.total_amount)
        }
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.post(url, payment_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['payment_successful'])
        self.assertIn('error', response.data)
        
        # Verify order status not changed
        self.order.refresh_from_db()
        self.assertEqual(self.order.status, 'pending')


class PaymentValidationTestCase(TestCase):
    """Test payment validation logic"""
    
    def test_card_number_validation(self):
        """Test credit card number validation"""
        from orders.serializers import PaymentSerializer
        
        # Valid card numbers
        valid_cards = [
            '4111111111111111',  # Visa
            '5555555555554444',  # MasterCard
            '378282246310005',   # Amex
        ]
        
        for card_number in valid_cards:
            serializer = PaymentSerializer(data={
                'payment_method': 'credit_card',
                'card_number': card_number,
                'expiry_month': '12',
                'expiry_year': '2025',
                'cvv': '123',
                'amount': '100.00'
            })
            self.assertTrue(serializer.is_valid(), f"Card {card_number} should be valid")
        
        # Invalid card numbers
        invalid_cards = [
            '1234',           # Too short
            'abcd1234567890', # Contains letters
            '0000000000000000', # All zeros
            '1111111111111111', # Invalid checksum
        ]
        
        for card_number in invalid_cards:
            serializer = PaymentSerializer(data={
                'payment_method': 'credit_card',
                'card_number': card_number,
                'expiry_month': '12',
                'expiry_year': '2025',
                'cvv': '123',
                'amount': '100.00'
            })
            self.assertFalse(serializer.is_valid(), f"Card {card_number} should be invalid")
    
    def test_expiry_date_validation(self):
        """Test card expiry date validation"""
        from orders.serializers import PaymentSerializer
        from datetime import datetime
        
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        # Valid future date
        serializer = PaymentSerializer(data={
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '12',
            'expiry_year': str(current_year + 1),
            'cvv': '123',
            'amount': '100.00'
        })
        self.assertTrue(serializer.is_valid())
        
        # Past date should be invalid
        serializer = PaymentSerializer(data={
            'payment_method': 'credit_card',
            'card_number': '4111111111111111',
            'expiry_month': '01',
            'expiry_year': str(current_year - 1),
            'cvv': '123',
            'amount': '100.00'
        })
        self.assertFalse(serializer.is_valid())
    
    def test_cvv_validation(self):
        """Test CVV validation"""
        from orders.serializers import PaymentSerializer
        
        # Valid CVVs
        valid_cvvs = ['123', '456', '789']
        
        for cvv in valid_cvvs:
            serializer = PaymentSerializer(data={
                'payment_method': 'credit_card',
                'card_number': '4111111111111111',
                'expiry_month': '12',
                'expiry_year': '2025',
                'cvv': cvv,
                'amount': '100.00'
            })
            self.assertTrue(serializer.is_valid(), f"CVV {cvv} should be valid")
        
        # Invalid CVVs
        invalid_cvvs = ['12', '1234', 'abc', '']
        
        for cvv in invalid_cvvs:
            serializer = PaymentSerializer(data={
                'payment_method': 'credit_card',
                'card_number': '4111111111111111',
                'expiry_month': '12',
                'expiry_year': '2025',
                'cvv': cvv,
                'amount': '100.00'
            })
            self.assertFalse(serializer.is_valid(), f"CVV {cvv} should be invalid")
