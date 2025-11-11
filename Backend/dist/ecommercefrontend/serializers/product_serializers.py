# ecommercefrontend/serializers/product_serializers.py
from rest_framework import serializers
from ..models import Product, CartItem, Category 

class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True) # 🆕 Category Name
    # Product Card Requirement: is_in_cart, is_in_wishlist 

    #  Product Card lo Cart Status chudaniki (Optional: Advanced Implementation)
    is_in_cart = serializers.SerializerMethodField()
    cart_item_id = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'name', 'description', 'price', 'image', 'is_available', 
            'category', 'category_name', 'is_in_cart', 'cart_item_id'
        ]

    def get_is_in_cart(self, obj):
        # Request lo user untey, aha user  cart lo e product undho leydho check chaysthundhi
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            # actual cart check logic (Simple dummy implementation)
            # return CartItem.objects.filter(cart__user=request.user, product=obj).exists() 
            return False 
        return False
    
    def get_cart_item_id(self, obj):
        # here cart_item id ni return chayali (Remove from Cart)
        return None
        
# Category List
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']