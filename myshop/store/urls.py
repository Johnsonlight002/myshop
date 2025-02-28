from django.urls import path
from .views import home, add_to_cart, remove_from_cart
from . import views
from .views import add_to_cart

urlpatterns = [
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name='checkout'),
    path('payment/', views.payment, name='payment'),
    path('charge/', views.charge, name='charge'),  # Stripe charge endpoint
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path("add-to-cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:product_id>/", remove_from_cart, name="remove_from_cart"),
]







