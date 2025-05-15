from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart_view'),  # Ensure this is present
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('increase_quantity/<int:product_id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease_quantity/<int:product_id>/', views.decrease_quantity, name='decrease_quantity'),

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup_view, name='signup'),

    path('checkout/', views.checkout_view, name='checkout'),
    path('order-summary/<int:order_id>/', views.order_summary, name='order_summary'),
    path('order_success/', views.order_success, name='order_success'),

    path('clear_session/', views.clear_session, name='clear_session'),
    path('dummy_payment/<int:order_id>/', views.dummy_payment, name='dummy_payment'),
    path('payment_success/<int:order_id>/', views.payment_success, name='payment_success'),

]
