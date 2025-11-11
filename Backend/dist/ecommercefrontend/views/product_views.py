# ecommercefrontend/views/product_views.py
from rest_framework import generics
from rest_framework.permissions import AllowAny 
from ..models import Product, Category
from ..serializers.product_serializers import ProductSerializer, CategorySerializer

# ----------------- 🆕 Product List View (Excludes Electronics) -----------------
class ProductListView(generics.ListAPIView):
    serializer_class = ProductSerializer
    permission_classes = [AllowAny] 

    def get_queryset(self):
        try:
            electronics_category = Category.objects.get(name__iexact='Electronics')
            exclude_id = electronics_category.id
        except Category.DoesNotExist:
            exclude_id = None

        queryset = Product.objects.filter(is_available=True)
        
        if exclude_id:
            queryset = queryset.exclude(category__id=exclude_id)
            
        return queryset.order_by('name')

# 🆕 Category List View
class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

# Product Detail View (unchanged)
class ProductDetailView(generics.RetrieveAPIView):
    #(old ProductDetailView code)
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    lookup_field = 'pk'