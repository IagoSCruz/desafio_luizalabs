# processador/serializers.py
from rest_framework import serializers
from .models import User, Order, Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['product_id', 'value']

class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    date = serializers.DateField(source='purchase_date') # Renomeia o campo na saída
    total = serializers.DecimalField(source='total_value', max_digits=12, decimal_places=2)

    class Meta:
        model = Order
        fields = ['order_id', 'date', 'total', 'products']

class UserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['user_id', 'name', 'orders']