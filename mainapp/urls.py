from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('contact/', views.contact, name='contact'),
    path('categories/', views.category, name='categories'),
    path('categories/<slug:slug>/', views.categories, name='categories'),
    path('products/<slug:slug>/', views.product, name='product'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.Search.as_view(), name='search'),
    path('accounts/logout/', views.logout, name='account_logout'),
    path('accounts/login/', views.signin, name='account_signin'),
    path('accounts/signup/', views.signup, name='account_signup'),
    path('my_orders/', views.order, name='order')
]
