from django.contrib import admin
from .models import *

admin.site.register(Banner)
admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(Seller)
admin.site.register(ProductSeller)
admin.site.register(BidProduct)
admin.site.register(BidInfo)
admin.site.register(BidResult)

