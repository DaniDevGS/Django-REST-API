from django.urls import path
from .views import ItemListView

urlpatterns = [
    path('products/', ItemListView.as_view(), name='products-list'),
]