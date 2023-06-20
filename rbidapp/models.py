from django.db import models
from django.contrib.auth.models import User

class Banner(models.Model):
    b_img = models.ImageField(upload_to = "banner_image/")
    title = models.CharField(max_length = 100, default='' )
    description = models.CharField(max_length = 300 , default='')
    link=models.CharField(max_length = 100, default='')
    class Meta:
        verbose_name_plural='Banners'
    def __str__(self):
        return self.title
        
class Category(models.Model):
	title = models.CharField(max_length = 100)
	c_img = models.ImageField(upload_to = "category_image/")
	class Meta:
		verbose_name_plural='Category'
	def __str__(self):
		return self.title
        
class Product(models.Model):
    name = models.CharField(max_length = 200)
    img1 = models.ImageField(upload_to = "product_image/",null=True)
    img2 = models.ImageField(upload_to = "product_image/",null=True)
    description = models.CharField(max_length = 400,default='')
    about = models.TextField()
    category =  models.ForeignKey(Category , on_delete = models.CASCADE , default='')
    price = models.PositiveIntegerField(default=0)
    offer = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Product'

   
    def __str__(self):
        return self.name
        
        
class ProductSeller(models.Model):
    seller = models.ForeignKey(User , on_delete = models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    p_name = models.CharField(max_length=100,default='')
    p_catog = models.CharField(max_length=100,default='')
    p_price = models.PositiveIntegerField(default=0)
    class Meta:
        verbose_name_plural='ProductSeller'

    
    
        
RATE = (
    (1,'1'),
    (2,'2'),
    (3,'3'),
    (4,'4'),
    (5,'5'),
) 
class Review(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product , on_delete = models.CASCADE)
    comment = models.TextField()
    rating=models.CharField(choices=RATE,max_length=150)
    class Meta:
        verbose_name_plural='Reviews'

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    p_name = models.CharField(max_length = 200, default='')
    p_img = models.CharField(max_length = 200, default='')
    p_id = models.PositiveIntegerField( default=0)
    p_price = models.PositiveIntegerField( default=0)
    p_qty = models.PositiveIntegerField()
    class Meta:
        verbose_name_plural='Cart'
        
class Seller(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural='Seller'
       

class BidProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    b_name = models.CharField(max_length = 200, default='')
    b_img = models.CharField(max_length = 200, default='')
    b_about = models.TextField()
    b_price = models.PositiveIntegerField( default=0)
    b_qty = models.PositiveIntegerField()
    b_expiry = models.DateTimeField()
    
    class Meta:
        verbose_name_plural='BidProduct'
        
        
        
class BidInfo(models.Model):
    bs_product = models.ForeignKey(BidProduct , on_delete = models.CASCADE , default='')
    bs_seller = models.ForeignKey(User,on_delete=models.CASCADE)
    bs_price = models.PositiveIntegerField()
    class Meta:
        verbose_name_plural='BidInfo'
        
class BidResult(models.Model):
    buyer = models.ForeignKey(User,on_delete=models.CASCADE, null=True , related_name='buyer' )
    name = models.CharField(max_length = 200, default='')
    qty = models.PositiveIntegerField()
    img = models.CharField(max_length = 200, default='')
    price = models.PositiveIntegerField()
    about = models.TextField()
    expiry = models.DateTimeField()
    seller1 = models.ForeignKey(User,on_delete=models.CASCADE,  null=True , related_name='seller1' )
    seller1_price = models.PositiveIntegerField()
    
    class Meta:
        verbose_name_plural='BidResult'

    
    
        
        
    
        
        