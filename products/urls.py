from django.urls import path
from .views import ItemListView, signup_api, signout_api, signin_api

urlpatterns = [
    path('products/', ItemListView.as_view(), name='products-list'),

    # New API Authentication Endpoints
    path('signup/', signup_api, name='api-signup'),
    path('signin/', signin_api, name='api-signin'),
    path('signout/', signout_api, name='api-signout'),
]