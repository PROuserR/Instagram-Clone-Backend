from django.urls import path
from .views import *

app_name = 'shop'
urlpatterns = [
    path('get_products/<str:shop_name>', get_products, name='get_products'),
    path('get_product/<str:product_name>', get_product, name='get_product'),
    path('create_stripe_checkout_session/', create_stripe_checkout_session, name='create_stripe_checkout_session'),
    path('stripe_webook/', stripe_webhook, name='stripe_webhook'),
]