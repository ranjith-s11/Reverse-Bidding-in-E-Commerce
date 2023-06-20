
from django.urls import path , include
from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home,name = 'home'),
    path('seller', views.seller,name = 'seller'),
    path('category', views.cat_list,name = 'category-list'),
    path('product', views.product_list,name = 'product-list'),
    path('search-result', views.search_result,name = 'search-result'),
    path('cat-product/<int:cat_id>', views.category_product,name = 'category-product-<int:cat_id>'),
    path('product/<int:product_id>', views.product_detail,name = 'product-<int:product_id>'),
    path('accounts/signup/',views.signup,name='signup'),
    path('accounts/seller-signup/',views.seller_signup,name='seller-signup'),
    path('add-review/<int:product_id>', views.add_review, name='add-review'),
    path('cart/<int:p_id>', views.add_cart, name='add-cart'),
    path('cart', views.cart, name='cart'),
    path('delete-cart/<int:c_id>', views.delete_cart, name='delete-cart'),
    path('product-upload', views.product_upload, name='product-upload'),
    path('seller-product', views.seller_product, name='seller-product'),
    path('bid-product/<int:p_id>', views.bid_product, name='bid-product'),
    path('bided-list', views.bided_list , name='bided-list'),
    path('delete-bided/<int:b_id>', views.delete_bided, name='delete-bided'),
    path('offers', views.offers_list,name = 'offers-list'),
    path('offer/<int:b_id>', views.offers_detail,name = 'offer-<int:b_id>'),
    path('add-bid/<int:b_id>', views.add_bid, name='add-bid'),
    path('delete-bid/<int:b_id>', views.delete_bid, name='delete-bid'),
    path('delete-bid-list/<int:b_id>', views.delete_bid_cart, name='delete-bid-list'),
    path('seller-bid-list', views.seller_bid_list, name='seller-bid-list'),
    path('get-bid-result/<int:b_id>', views.get_bid_result, name='get-bid-result'),
    path('bid-result', views.bid_result, name='bid-result'),

]

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)