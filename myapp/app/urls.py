from django.contrib import admin
from django.urls import path
from . import views
app_name = 'app'
urlpatterns = [
    path('', views.index),
    # is a class based view needs .as_view()
    path('products/', views.ProductListView.as_view(), name="products"),
    path('products/<int:pk>/', views.ProductDetailView.as_view(),
         name="product_detail"),
    path('products/add/', views.ProductCreateView.as_view(), name="add_product"),
    path('products/update/<int:pk>/',
         views.ProductUpdateView.as_view(), name="update_product"),
    path('products/delete/<int:pk>/',
         views.ProductDeleteView.as_view(), name="delete_product"),
    path('products/search/', views.SearchView.as_view(), name='search'),
    path('products/mylistings', views.my_listing, name="mylistings"),

]
