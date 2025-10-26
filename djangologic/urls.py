"""
URL configuration for djangologic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path, include
from products import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.signout, name='logout'),
    path('signin/', views.signin, name='signin'),
    path('products/', views.products, name='products'),
    path('products_to_send/', views.products_to_send, name='products_to_send'),
    path('product/create/', views.create_product, name='create_product'),
    path('products/<int:products_id>/', views.product_detail, name='products_detail'),
    path('api/', include('products.urls')),
    # urls.py
    path('products/<int:products_id>/complete', views.sent_product, name='complete_products'), # type: ignore
    path('products/<int:products_id>/delete', views.delete_product, name='delete_products'), # <-- Asegúrate de la coma # type: ignore
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)