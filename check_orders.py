import os
import django
import sys

sys.path.append('/home/fedora/Projects/alx-project-nexus')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_backend.settings')
django.setup()

from orders.models import Order
from users.models import User

# Check unpaid orders
orders = Order.objects.filter(payment_status='unpaid')[:5]
print(f"Unpaid orders available for testing: {orders.count()}")
for order in orders:
    print(f"  - Order {order.id}: status='{order.status}', payment='{order.payment_status}', user='{order.user.email}'")

print("\nAll orders:")
all_orders = Order.objects.all()[:5]
for order in all_orders:
    print(f"  - Order {order.id}: status='{order.status}', payment='{order.payment_status}', user='{order.user.email}'")
