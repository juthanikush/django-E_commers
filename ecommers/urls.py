from django.urls import path
from ecommers import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('',views.Index.as_view(),name='home'),
    path('product-detail/<int:pk>',views.ProductDetailsView.as_view(),name='product-details'),
    path('login',views.login.as_view(),name='login'),
    path('account',views.account.as_view(),name='account'),
    path('verifi',views.verifi.as_view(),name='verifi'),
    path('logout/',views.logout,name='logout'),
    path('thank_you/',views.thank_you,name='thank_you'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('wish_remove/',views.wish_remove,name='wish_remove'),
    path('my_order/',views.my_order,name='my_order'),
    path('wishlist_main/',views.wishlist_main,name='wishlist_main'),
    path('mycart/',views.mycart,name='mycart'),
    path('cart_incerment/',views.cart_incerment,name='cart_incerment'),
    path('cart_decrement/',views.cart_decrement,name='cart_decrement'),
    path('coupon_code/',views.couponcode,name='coupon_code'),
    path('chack_out/',views.checkout,name='check_out'),
    path('purchace',views.purchace.as_view(),name='purchace'),
    path('remove_addtocart',views.remove_addtocart,name='remove_addtocart'),
    path('addtocart/',views.addtocart.as_view(),name='addtocart'),
]+ static (settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)