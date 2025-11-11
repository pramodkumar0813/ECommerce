"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# ecommercefrontend/urls.py

from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    # 👇 Admin Panel కోసం ఈ లైన్ తప్పనిసరి
    path('admin/', admin.site.urls),
    # Auth URLs (Includes Send OTP, Verify OTP)
    path('', include('ecommercefrontend.urls.auth_urls')),
    
    # Product URLs (unchanged from last time)
    path('', include('ecommercefrontend.urls.product_urls')),
    
    # 🆕 Cart URLs
    path('', include('ecommercefrontend.urls.cart_urls')),
]

