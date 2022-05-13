# from django.contrib import admin
# from .models import UserWishlist, WishlistProduct

# # Register your models here.
# admin.site.register(UserWishlist)
# admin.site.register(WishlistProduct)
from django.contrib import admin
from wishlist.models import WishList


admin.site.register(WishList)