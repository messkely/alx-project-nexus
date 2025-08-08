from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.db import transaction
from django.core.exceptions import PermissionDenied
from .models import Order, OrderItem
from .serializers import (
    OrderSerializer, 
    CreateOrderSerializer, 
    OrderStatusUpdateSerializer,
    PaymentSerializer
)
from catalog.models import Product
from cart.models import Cart


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class CreateOrderView(APIView):
    permission_classes = [IsAuthenticated]

    @transaction.atomic
    def post(self, request):
        serializer = CreateOrderSerializer(data=request.data)
        if serializer.is_valid():
            items_data = serializer.validated_data['items']
            
            # Calculate total amount
            total_amount = 0
            order_items = []
            
            for item_data in items_data:
                product = Product.objects.get(id=item_data['product_id'])
                quantity = item_data['quantity']
                unit_price = product.price
                subtotal = unit_price * quantity
                total_amount += subtotal
                
                order_items.append({
                    'product': product,
                    'quantity': quantity,
                    'unit_price': unit_price,
                    'subtotal': subtotal
                })
            
            # Create order
            order = Order.objects.create(
                user=request.user,
                total_amount=total_amount
            )
            
            # Create order items
            for item in order_items:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    quantity=item['quantity'],
                    unit_price=item['unit_price'],
                    subtotal=item['subtotal']
                )
            
            # Clear user's cart if it exists
            try:
                cart = Cart.objects.get(user=request.user)
                cart.items.all().delete()
            except Cart.DoesNotExist:
                pass
            
            return Response(
                OrderSerializer(order).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You don't have permission to access this order.")
        return obj


class CancelOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        # Check if order can be cancelled
        if order.status in ['completed', 'delivered', 'cancelled']:
            return Response(
                {'error': f'Cannot cancel order. Order is already {order.status}.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if order.status == 'shipped':
            return Response(
                {'error': 'Cannot cancel shipped order. Please contact customer service.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cancel the order
        order.status = 'cancelled'
        order.save()
        
        return Response({
            'message': 'Order cancelled successfully.',
            'order': OrderSerializer(order).data
        }, status=status.HTTP_200_OK)


class OrderStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        if order.user != request.user:
            raise PermissionDenied("You don't have permission to view this order.")
            
        return Response({
            'order_id': order.id,
            'status': order.status,
            'payment_status': order.payment_status
        })


class TrackOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        # Mock tracking data - in real app this would come from shipping provider
        tracking_data = {
            'order_id': order.id,
            'status': order.status,
            'tracking_number': f'TRK{order.id:08d}',
            'estimated_delivery': None,
            'tracking_events': [
                {
                    'date': order.created_at.isoformat(),
                    'status': 'Order placed',
                    'description': 'Your order has been placed successfully.'
                }
            ]
        }
        
        if order.status == 'completed':
            tracking_data['tracking_events'].append({
                'date': order.updated_at.isoformat(),
                'status': 'Order completed',
                'description': 'Your order has been completed.'
            })
        
        return Response(tracking_data)


class OrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Order.objects.none()
        return Order.objects.filter(user=self.request.user).order_by('-created_at')


class ProcessPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        if order.payment_status == 'paid':
            return Response(
                {'error': 'Order already paid.'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            # Mock payment processing - in real app this would integrate with payment gateway
            payment_method = serializer.validated_data['payment_method']
            
            # Simulate payment processing
            order.payment_status = 'paid'
            order.status = 'completed'
            order.save()
            
            return Response({
                'message': 'Payment processed successfully.',
                'payment_method': payment_method,
                'order': OrderSerializer(order).data
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmPaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk, user=request.user)
        
        # Mock payment confirmation
        if order.payment_status == 'unpaid':
            order.payment_status = 'paid'
            order.status = 'completed'
            order.save()
        
        return Response({
            'message': 'Payment confirmed.',
            'order': OrderSerializer(order).data
        })


class AdminOrderListView(generics.ListAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]


class UpdateOrderStatusView(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        serializer = OrderStatusUpdateSerializer(order, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response(OrderSerializer(order).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
