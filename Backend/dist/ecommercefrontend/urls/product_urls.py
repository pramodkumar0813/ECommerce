# ecommercefrontend/urls/product_urls.py
from django.urls import path
from ecommercefrontend.views.product_views import ProductListView, ProductDetailView, CategoryListView # 🆕

urlpatterns = [
    # GET: /products/list/ (Electronics excluded)
    path('products/list/', ProductListView.as_view(), name='product_list'),
    
    # GET: /products/categories/
    path('products/categories/', CategoryListView.as_view(), name='category_list'), # 🆕 Category List
    
    # GET: /products/<id>/
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]