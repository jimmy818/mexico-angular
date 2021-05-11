from django.urls import path
from . import views


urlpatterns = [
    path('customer/<int:pk>/', views.CustomerView.as_view(), name='customer-detail'),
    path('products/', views.ListProductsView.as_view(), name='product-list'),
    path('products/<str:pk>/', views.RetrieveProductView.as_view(), name='product-detail'),
    path('products/<str:pk>/prices/', views.ListProductPricesView.as_view(), name='product-prices'),
    path('prices/<str:pk>/', views.RetrievePriceView.as_view(), name='price-detail'),
]
