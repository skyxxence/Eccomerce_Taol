from django.urls import path
from .views import *

urlpatterns = [
    path('home', homeview, name='go-home'), 
    path('add', vendor_add_product, name='vendor-add-product'), 
    path('vendor_product_list', vendor_product_list, name='vendor-product-list'), 
    path('vendor_edit_product/<int:product_id>/', vendor_edit_product, name='vendor-edit-product'),
    path('vendor-product-details/<int:product_id>/', vendor_product_details, name='vendor-product-details'),
    path('vendor-delete-product/<int:product_id>/', vendor_delete_product, name='vendor-delete-product'),
    path('category/<int:category_i>/', category_detail, name='category-detail'), 
    
    path('category/<str:category_name>/', products_by_category, name='get-by-category'), 
    path('subcategory/<str:subcategory_name>/', products_by_subcategory, name='get-by-subcategory'), 
    
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add-to-cart'),
    path('cart-view', view_cart, name='view-cart'), 
    path('product-details/<int:product_id>/', product_details, name='product-details'),
    
    ]
    