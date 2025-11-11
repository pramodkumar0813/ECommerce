# ecommercefrontend/views/cart_views.py
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from ..models import Cart, CartItem, Product
from ..serializers.cart_serializers import CartSerializer, AddToCartSerializer

# ---------- 🆕 Add To Cart View (with Profile Check) ----------
class AddToCartView(generics.GenericAPIView):
    serializer_class = AddToCartSerializer
    permission_classes = [IsAuthenticated] 

    def post(self, request, *args, **kwargs):
        user = request.user
        
        # ⚠️ Profile Completion Restriction Check 
        if not user.is_profile_complete:
            return Response(
                {"detail": "Profile incomplete. Please update your profile (address, name, etc.) before adding products to cart."},
                status=status.HTTP_403_FORBIDDEN # 403 Forbidden
            )

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product_id = serializer.validated_data['product_id']
        quantity = serializer.validated_data['quantity']
        
        # last login cart details
        cart, created = Cart.objects.get_or_create(user=user, is_active=True)
        product = get_object_or_404(Product, id=product_id)

        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            defaults={'quantity': quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)


# ---------- 🆕 View/Retrieve Cart ----------
class CartDetailView(generics.RetrieveAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        # presnt user active cart only can return
        return get_object_or_404(Cart, user=self.request.user, is_active=True)