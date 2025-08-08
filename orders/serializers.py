from rest_framework import serializers
from .models import Order, OrderItem
from catalog.serializers import ProductSerializer
from users.serializers import AddressSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_id', 'quantity', 'unit_price', 'subtotal']
        read_only_fields = ['id', 'unit_price', 'subtotal']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    user_email = serializers.CharField(source='user.email', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'user', 'user_email', 'status', 'payment_status', 
            'total_amount', 'created_at', 'updated_at', 'items'
        ]
        read_only_fields = ['id', 'user', 'total_amount', 'created_at', 'updated_at']


class CreateOrderSerializer(serializers.Serializer):
    items = serializers.ListField(
        child=serializers.DictField(),
        allow_empty=False
    )

    def validate_items(self, value):
        from catalog.models import Product
        
        if not value:
            raise serializers.ValidationError("Order must contain at least one item.")
        
        for item in value:
            if 'product_id' not in item or 'quantity' not in item:
                raise serializers.ValidationError("Each item must have product_id and quantity.")
            
            try:
                product = Product.objects.get(id=item['product_id'])
            except Product.DoesNotExist:
                raise serializers.ValidationError(f"Product with id {item['product_id']} does not exist.")
            
            if item['quantity'] <= 0:
                raise serializers.ValidationError("Quantity must be greater than 0.")
        
        return value


class OrderStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']

    def validate_status(self, value):
        if value not in ['pending', 'completed', 'failed']:
            raise serializers.ValidationError("Invalid status.")
        return value


class PaymentSerializer(serializers.Serializer):
    payment_method = serializers.CharField(max_length=50)
    payment_details = serializers.DictField(required=False)

    def validate_payment_method(self, value):
        allowed_methods = ['card', 'credit_card', 'debit_card', 'paypal', 'bank_transfer']
        if value not in allowed_methods:
            raise serializers.ValidationError("Invalid payment method.")
        return value
