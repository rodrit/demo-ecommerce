from .models import Product, Order, OrderDetail
from rest_framework import viewsets
from .serializers import ProductSerializer, OrderSerializer, OrderDetailSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


class ProductViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer



class OrderViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
