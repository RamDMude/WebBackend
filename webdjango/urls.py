"""webdjango URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

import Webback.views

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/users/', Webback.views.Users),
    path('api/login/', Webback.views.login),
    path('api/menswear/',Webback.views.menswear),
    path('api/mensproduct/', Webback.views.mensproduct),
    path('api/womenswear/',Webback.views.womenswear),
    path('api/womensproduct/', Webback.views.womensproduct),
    path('api/watches/',Webback.views.watches),
    path('api/watchesproduct/', Webback.views.watchesproduct),
    path('api/cart/', Webback.views.showcart),
    path('api/addtocart/', Webback.views.addtocart),
    path('api/removefromcart/', Webback.views.removefromcart),
    path('api/orderhist/', Webback.views.orderfunc),
    path('api/orders/', Webback.views.showorders),
    path('api/fetchdetails/', Webback.views.fetchdetails),
    path('api/changedetails/', Webback.views.changedetails),
]
