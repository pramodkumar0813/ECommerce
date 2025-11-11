# ecommercefrontend/urls/cart_urls.py
from django.urls import path
from ecommercefrontend.views.cart_views import AddToCartView, CartDetailView

urlpatterns = [
    # POST: /api/cart/add/
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    # GET: /api/cart/details/
    path('cart/details/', CartDetailView.as_view(), name='cart_details'),
]