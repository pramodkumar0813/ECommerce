# ecommercefrontend/serializers/cart_serializers.py
from rest_framework import serializers
from ..models import Cart, CartItem, Product

class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_name', 'product_price', 'quantity', 'total_price']
        read_only_fields = ['product'] #add to cart lo product ni views lo handle chaysthamu

    def get_total_price(self, obj):
        return obj.total_price()


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_cart_value = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'total_cart_value']

    def get_total_cart_value(self, obj):
        total = sum(item.total_price() for item in obj.items.all())
        return total

# ---------- 🆕 Add to Cart Serializer (Input) ----------
class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate_product_id(self, value):
        try:
            Product.objects.get(id=value, is_available=True)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist or is unavailable.")
        return value