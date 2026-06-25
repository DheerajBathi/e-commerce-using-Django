from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.store_view, name='store_view'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('add-review/<slug:slug>/', views.add_review, name='add_review'),
    path('cart/', views.cart_view, name='cart_view'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/update/', views.cart_update, name='cart_update'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.checkout_view, name='checkout_view'),
    path('order-success/<int:order_id>/', views.order_success, name='order_success'),
]
