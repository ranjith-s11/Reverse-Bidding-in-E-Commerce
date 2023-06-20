from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import *
from .forms import *
from django.contrib.auth import authenticate , login
from django.conf import settings
from django.core.mail import send_mail

import datetime
from django.contrib.auth.decorators import login_required
from django.utils import timezone

@login_required
def home(request):
    sellers = Seller.objects.get(user=request.user)
    if sellers.status:
        return render(request, 'seller-home.html' ,{})
    categories = Category.objects.all().order_by('-id')[:3]
    banners = Banner.objects.all().order_by('-id')
    products = Product.objects.all().order_by('-id')[:3]
    return render (request, 'home.html',{'banners':banners,'categories':categories,'products':products,'sellers':sellers})
    
@login_required
def seller(request):
    return render(request, 'seller-home.html' ,{})

def cat_list(request):
    categories = Category.objects.all().order_by('id')
    return render (request, 'category.html',{'categories':categories})

def product_list(request):
    products = Product.objects.all().order_by('id')
    return render (request, 'product.html',{'products':products})
    
def category_product(request,cat_id):
    category = Category.objects.get(id=cat_id)
    products = Product.objects.filter(category=category).order_by('id')
    return render (request, 'product.html',{'products':products})
    
@login_required    
def product_detail(request,product_id):
    data = Product.objects.get(id=product_id)
    reviewform = ReviewForm()
    recommendeds = Product.objects.filter(category=data.category).order_by('id').exclude(id=product_id)[:4]
    reviews = Review.objects.filter(product=data).order_by('id')[:3]
    check = Review.objects.filter(user=request.user , product=data).count()
    if check==0:
        eligible = True
    else:
        eligible = False
    return render (request, 'product-detail.html',{'data':data,'recommendeds':recommendeds,'reviewform':reviewform,'reviews':reviews,'eligible':eligible})
    
def search_result(request):
    searchy = request.GET['searchy']
    products = Product.objects.filter(name__icontains=searchy,).order_by('id')
    return render (request, 'search-page.html',{'products':products})
    
def signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            email=form.cleaned_data.get('email')
            user=authenticate(username=username,password=pwd)
            login(request, user)
            
            user=request.user
            seller=Seller.objects.create(
            user=user,
            status=False
            )

            return redirect('home')
    form=SignupForm
    return render(request, 'registration/signup.html',{'form':form})
    
    
def seller_signup(request):
    if request.method=='POST':
        form=SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password1')
            email=form.cleaned_data.get('email')
            user=authenticate(username=username,password=pwd)
            login(request, user)
            
            user=request.user
            seller=Seller.objects.create(
            user=user,
            status=True
            )
            


            return redirect('seller')
    form=SignupForm
    return render(request, 'registration/seller-signup.html',{'form':form})
    
@login_required
def add_review(request,product_id):
	product=Product.objects.get(pk=product_id)
	user=request.user
	review=Review.objects.create(
		user=user,
		product=product,
		comment =request.POST['comment'],
		rating=request.POST['rating'],
		)
        
	return redirect('http://localhost:8000/product/'+str(product_id))
    
@login_required
def add_cart(request,p_id):
    p_qty = request.GET["quantity"]
    p_name = request.GET["p_name"]
    p_price = request.GET["p_price"]
    p_img = request.GET["p_img"]
    product = Product.objects.get(pk=p_id)
    user=request.user
    cart=Cart.objects.create(
		user=user,
		p_id=p_id,
        p_name=p_name,
        p_price=p_price,
		p_qty=p_qty,
        p_img=p_img
		)
        
    return redirect('http://localhost:8000/cart')

@login_required
def cart(request):
    user=request.user
    carts=Cart.objects.filter(user=user).order_by('id')
    tot_amt = 0
    for car_t in carts:
        tot_amt = tot_amt + car_t.p_qty * car_t.p_price
    return render(request, 'cart.html',{'carts':carts,'tot_amt':tot_amt})
    
@login_required
def delete_cart(request,c_id):
    Cart.objects.get(pk=c_id).delete()
    return redirect('http://localhost:8000/cart')
    
@login_required
def product_upload(request):
    
    if request.method=='POST':
        form=ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save()
            
            user= request.user
            product = ProductSeller.objects.create(
                seller = user,
                product = product,
                p_name = product.name,
                p_catog = product.category,
                p_price = product.price,
            )
            
            return redirect('home')
    form=ProductForm
    return render(request, 'product-upload.html',{'form':form})
    

@login_required
def seller_product(request):
    user=request.user
    products = ProductSeller.objects.filter(seller=user)
    return render (request, 'test.html',{'products':products})
    
@login_required
def bid_product(request,p_id):
    user = request.user
    b_name = request.GET["b_name"]
    b_price = request.GET["b_price"]
    b_img = request.GET["b_img"]
    b_about = request.GET["b_about"]
    b_day = request.GET["b_day"]
    b_qty = request.GET["b_qty"]
    b_day = int(b_day)
    b_expiry = timezone.now() + datetime.timedelta(hours=b_day*24)
    
    bidproduct=BidProduct.objects.create(
		user=user,
        b_name=b_name,
        b_about=b_about,
        b_price=b_price,
		b_qty=b_qty,
        b_img=b_img,
        b_expiry = b_expiry,
		)
        
    return redirect('http://localhost:8000/product')
    
@login_required
def bided_list(request):
    user=request.user
    bideds = BidProduct.objects.filter(user=user)
    now_st = timezone.now()
    cbids = bideds.filter(b_expiry__lt=now_st)
    return render(request,'bided-list.html',{'bideds':bideds,'cbids':cbids})
    
@login_required
def delete_bided(request,b_id):
    bided = BidProduct.objects.filter(pk=b_id)
    bided.delete()
    return redirect('http://localhost:8000/bided-list')
    
@login_required
def offers_list(request):
    offers = BidProduct.objects.all()
    return render (request, 'offer-list.html',{'offers':offers})
    
@login_required
def offers_detail(request,b_id):

    dt = timezone.now()
    bproduct = BidProduct.objects.get(pk=b_id)
    if bproduct.b_expiry <= dt:

        binfo = BidInfo.objects.filter(bs_product=bproduct).order_by('bs_price')[:1]
        
        sell = 0 
        for binf in binfo:
            sell = binf
            
        bidresult = BidResult.objects.create(
        
            buyer = bproduct.user,
            name = bproduct.b_name,
            qty = bproduct.b_qty,
            price = bproduct.b_price,
            img = bproduct.b_img,
            about = bproduct.b_about,
            expiry = bproduct.b_expiry,
            seller1 = sell.bs_seller,
            seller1_price = sell.bs_price,
            
            )
        bproduct.delete()
        return redirect('http://localhost:8000/offers')

    usery=request.user
    data = BidProduct.objects.get(pk=b_id)
    prcs = BidInfo.objects.filter(bs_product=data)
    return render (request, 'offer-detail.html',{'data':data,'prcs':prcs,'usery':usery})
    
@login_required
def add_bid(request,b_id):
    product=BidProduct.objects.get(pk=b_id)
    user=request.user
    bs_price = request.GET["bs_price"]
    bidinfo=BidInfo.objects.create(
		bs_seller=user,
		bs_product=product,
		bs_price =bs_price,
		)
    return redirect('http://localhost:8000/offer/'+str(b_id))
    
@login_required
def delete_bid(request,b_id):
    user=request.user
    product=BidProduct.objects.get(pk=b_id)
    bid=BidInfo.objects.filter(bs_product=product, bs_seller=user)
    bid.delete()
    return redirect('http://localhost:8000/offer/'+str(b_id))
    
@login_required  
def delete_bid_cart(request,b_id):
    user=request.user
    product=BidProduct.objects.get(pk=b_id)
    bid=BidInfo.objects.filter(bs_product=product, bs_seller=user)
    bid.delete()
    return redirect('http://localhost:8000/seller-bid-list')
    
@login_required   
def seller_bid_list(request):
    user=request.user
    datas = BidProduct.objects.filter(bidinfo__bs_seller=user)
    return render(request,'sellers-bid-cart.html',{'datas':datas})
    
@login_required
def get_bid_result(request,b_id):
    bproduct = BidProduct.objects.get(pk=b_id)
    binfo = BidInfo.objects.filter(bs_product=bproduct).order_by('bs_price')[:1]
    
    sell = 0 
    for binf in binfo:
        sell = binf
     

    bidresult = BidResult.objects.create(
        buyer = bproduct.user,
        name = bproduct.b_name,
        qty = bproduct.b_qty,
        price = bproduct.b_price,
        img = bproduct.b_img,
        about = bproduct.b_about,
        expiry = bproduct.b_expiry,
        seller1 = sell.bs_seller,
        seller1_price = sell.bs_price,
        ) 
    bproduct.delete()
    return redirect('http://localhost:8000/bided-list')
 
@login_required
def bid_result(request):
    user = request.user
    bidresults = BidResult.objects.filter(buyer = user)
    return render(request,"bid-result.html",{'bidresults':bidresults})