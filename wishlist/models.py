# from django.db import models
# from django.conf import settings
# from products.models import Product
# from django.contrib.auth.models import User

# # model for wishlist
# class UserWishlist(models.Model):
#     wishlist_name = models.CharField(max_length=30,null=True,blank=True)
#     wishlist_owner = models.ForeignKey(User, on_delete=models.CASCADE)

# class WishlistProduct(models.Model):
#     wishlist = models.ForeignKey(UserWishlist, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)

from django.db import models

from profiles.models import UserProfile
from products.models import Product


class WishList(models.Model):
    """
    Model to show all product items within the users wishlist
    """
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f'WishList ({self.user_profile})'