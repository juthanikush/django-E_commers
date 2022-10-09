from django.contrib import admin
from ecommers.models import User,placed_order,Products,wishlist_item,Add_to_cart,user_dateils,coupon_code
# Register your models here.
admin.site.register(User)
admin.site.register(Products)
admin.site.register(Add_to_cart)
admin.site.register(user_dateils)
admin.site.register(coupon_code)
admin.site.register(placed_order)
admin.site.register(wishlist_item)