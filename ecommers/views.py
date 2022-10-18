from ast import Add
from audioop import add
from itertools import product
from unicodedata import category
from urllib import response
import requests
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.db.models import Q
from django.views import View
from django.conf import settings
import random
from django.core.mail import send_mail
from .models import ( User,Add_to_cart,Products,placed_order,wishlist_item,user_dateils,coupon_code)
from instamojo_wrapper import Instamojo
#api
api=Instamojo(api_key=settings.API_KEY,auth_token=settings.AUTH_TOKEN,endpoint='https://test.instamojo.com/api/1.1/')
# Create your views here.

class Index(View):
    def get(self,request):
        products_m=Products.objects.filter(products_category='Men')
        products_w=Products.objects.filter(products_category='Women')
        products_e=Products.objects.filter(products_category='Electronics')
        if request.session.get('id',None):
            id=request.session['id']
            addtocart=Add_to_cart.objects.filter(uid=id).all()
            count=Add_to_cart.objects.filter(uid=id).count()
            total=0
            for a in addtocart:
                total+=a.qty*a.pid.products_price

            return render(request,'app/index.html',{'products_m':products_m,'products_w':products_w,'products_e':products_e,'addtocart':addtocart,'total':total,'count':count})
        else:
            total=0
            count=0
        return render(request,'app/index.html',{'products_m':products_m,'products_w':products_w,'products_e':products_e,'total':total,'count':count})

class ProductDetailsView(View):
    def get(self,request,pk):
        product=Products.objects.get(pk=pk);
        if request.session.get('id',None):
            id=request.session['id']
            addtocart=Add_to_cart.objects.filter(uid=id).all()
            count=Add_to_cart.objects.filter(uid=id).count()
            total=0
            for a in addtocart:
                total+=a.qty*a.pid.products_price

            return render(request,'app/product-detail.html',{'product':product,'total':total,'count':count})
        else:
            total=0
            count=0
        return render(request,'app/product-detail.html',{'product':product,'total':total,'count':count})


class login(View):
    def post(self,request):
        email=request.POST.get("email")
        password=request.POST.get("password")
        u=User.objects.filter(email=email).filter(password=password).filter(verify=1).get()
        k=User.objects.filter(email=email).filter(password=password).filter(verify=1).get()
        if u:
            request.session['name']=k.name
            request.session['id']=k.id
            return redirect('/')
        else:
            return redirect('/')


class account(View):
    def get(self,request):
        return render(request,'app/account.html')

    def post(self,request):
        name=request.POST.get("name")
        password=request.POST.get("password")
        email=request.POST.get('email')
        verify=0
        a=random.SystemRandom().randint(000000,999999)
        
        u=User(name=name,password=password,email=email,verify=verify,code=a)
        u.save();
        a=str(a)
        send_mail('Email Verificashion',a,settings.EMAIL_HOST_USER,[email,]);
        return render(request,'app/verifashion.html',{'msg':'Pleace Verify your Email Address'});

class verifi(View):
    def post(self,request):
        code=request.POST.get("code")
        u=User.objects.filter(code=code).exists()
        k=User.objects.filter(code=code).update(verify=1)
        if u:
            return render(request,'app/verifashion.html',{'msg':'Your Email id is verified'});
        else:
            return render(request,'app/verifashion.html',{'msg':'Please Enter Valied Code'});

def logout(request):
    request.session.pop("name")
    request.session.pop("id")
    return redirect('/')

class addtocart(View):
    def get(self,request):
        proid=request.GET['pro_id']
        qty=request.GET['qty']
        id=request.session['id']
        pro_id=Products.objects.get(id=proid)
        u_id=User.objects.get(id=id)
        a=Add_to_cart(uid=u_id,pid=pro_id,qty=qty)
        a.save()
        addtocart=Add_to_cart.objects.filter(uid=id).all()
        count=Add_to_cart.objects.filter(uid=id).count()
        total=0
        for a in addtocart:
            total+=a.qty*a.pid.products_price
        addtocart=Add_to_cart.objects.filter(uid=id).last()
        id=addtocart.id
        image=a.pid.products_Image
        img=str(image)
        qty=a.qty
        name=a.pid.products_name
        price=a.pid.products_price
        data={'status':'success','id':id,'qty':qty,'img':img,'name':name,'price':price,'total':total,'count':count}
        return JsonResponse(data)

    def post(self,request):
        proid=request.POST.get('pro_id')
        qty=request.POST.get('qty')
        id=request.session['id']
        pro_id=Products.objects.get(id=proid)
        u_id=User.objects.get(id=id)
        a=Add_to_cart(uid=u_id,pid=pro_id,qty=qty)
        a.save()
        return redirect('/')

def remove_addtocart(request):
    atc_id=request.GET['atc_id']
    c=Add_to_cart.objects.get(id=atc_id)
    c.delete()
    id=request.session['id']
    addtocart=Add_to_cart.objects.filter(uid=id).all()
    count=Add_to_cart.objects.filter(uid=id).count()
    total=0
    for a in addtocart:
        total+=a.qty*a.pid.products_price
    data={'status':'success','total':total,'count':count}
    return JsonResponse(data)

def mycart(request):
    id=request.session['id']
    addtocart=Add_to_cart.objects.filter(uid=id).all()
    b=Add_to_cart.objects.filter(uid=id).all()
    count=Add_to_cart.objects.filter(uid=id).count()
    total=0
    for i in b:
        temp=i.qty*i.pid.products_price
        total+=temp
    return render(request,'app/cart.html',{'addtocart':addtocart,'total':total,'count':count});

def cart_incerment(request):
    id=request.GET['id']
    c=Add_to_cart.objects.get(id=id)
    c.qty+=1
    pro_total=c.qty*c.pid.products_price
    c.save()
    id=request.session['id']
    addtocart=Add_to_cart.objects.filter(uid=id).all()
    total=0
    for a in addtocart:
        total+=a.qty*a.pid.products_price
    data={'status':'success','total':total,'pro_total':pro_total}
    return JsonResponse(data)

def cart_decrement(request):
    id=request.GET['id']
    c=Add_to_cart.objects.get(id=id)
    c.qty-=1
    qty=c.qty
    pro_total=c.qty*c.pid.products_price
    c.save()
    add_id=id
    id=request.session['id']
    addtocart=Add_to_cart.objects.filter(uid=id).all()
    total=0
    for a in addtocart:
        total+=a.qty*a.pid.products_price
    
    if qty==0:
        Add_to_cart.objects.filter(id=add_id).delete()
        count=Add_to_cart.objects.filter(uid=id).count()
        data={'status':'error','count':count,'total':total,'pro_total':pro_total}
        return JsonResponse(data)
    print('l')
    data={'status':'success','total':total,'pro_total':pro_total}
    return JsonResponse(data)
    
def couponcode(request):
    code=request.GET['code']
    count=0
    count=coupon_code.objects.filter(coupon_name=code).count()
    if count==0:
        print('j')
        data={'status':'error','msg':"Please Enter valid Coupon code"}
    else:
        print('h')
        id=request.session['id']
        addtocart=Add_to_cart.objects.filter(uid=id).all()
        total=0
        for a in addtocart:
            total+=a.qty*a.pid.products_price
        amount=coupon_code.objects.filter(coupon_name=code).get()
        coupon_code_amount=amount.coupon_price
        total=total-coupon_code_amount
        request.session['coupon_code_amount']=coupon_code_amount
        data={'status':'success','total':total}
    return JsonResponse(data)

def checkout(request):
    id=request.session['id']
    addtocart=Add_to_cart.objects.filter(uid=id).all()
    b=Add_to_cart.objects.filter(uid=id).all()
    count=Add_to_cart.objects.filter(uid=id).count()
    total=0
    for i in b:
        temp=i.qty*i.pid.products_price
        total+=temp
    count=Add_to_cart.objects.filter(uid=id).count()
    coupon_amount=0
    if request.session.get('coupon_code_amount',0):
        coupon_amount=request.session['coupon_code_amount']
    if coupon_amount:
        final_total=total-coupon_amount
    else:
        final_total=total
    

    return render(request,'app/checkout.html',{'count':count,'addtocart':addtocart,'sub_total':total,'final_total':final_total,'total':final_total})


class purchace(View):
    def post(self,request):
        first_name=request.POST.get('fn')
        last_name=request.POST.get('ln')
        phone=request.POST.get('phone')
        email=request.POST.get('email')
        address=request.POST.get('address')
        id=request.session['id']
        u_id=User.objects.get(id=id)
        ud=user_dateils(first_name=first_name,last_name=last_name,email=email,phone=phone,addresss=address,uid=u_id)
        ud.save()

        payment_type=request.POST.get('optionsRadios')
        if payment_type=='1':
            id=request.session['id']
            u_id=User.objects.get(id=id)
            addtocart=Add_to_cart.objects.filter(uid=id).all()
            total=0
            for i in addtocart:
                temp=i.qty*i.pid.products_price
                total+=temp

            coupon_amount=0
            if request.session.get('coupon_code_amount',0):
                coupon_amount=request.session['coupon_code_amount']
            if coupon_amount:
                final_total=total-coupon_amount
            else:
                final_total=total

            
            response=api.payment_request_create(
                amount=final_total,
                purpose='Order Process',
                buyer_name=first_name+' '+last_name,
                email=email,
                redirect_url='http://127.0.0.1:8000/thank_you/'
            )
            coupon_amount=0
            if request.session.get('coupon_code_amount',0):
                coupon_amount=request.session['coupon_code_amount']
            for i in addtocart:
                po=placed_order(uid=u_id,pid=i.pid,qty=i.qty,coupon_amount=coupon_amount,payment_request_id=response['payment_request']['id'],payment_id=1)
                po.save()
                Products.objects.filter(id=i.pid.id).update(products_qty=i.pid.products_qty-i.qty)
             

            Add_to_cart.objects.filter(uid=id).delete()
            request.session['coupon_code_amount']=0
            request.session.pop("coupon_code_amount")
            return redirect(response['payment_request']['longurl'])
        else:
            pass


def thank_you(request):
    total=0
    count=0
    return render(request,'app/thank_you.html',{'total':total,'count':count})


def wishlist(request):
    id=request.session['id']
    user_id=User.objects.get(id=id)
    id=request.GET['id']
    product=Products.objects.get(id=id)
    wl=wishlist_item(uid=user_id,pid=product)
    wl.save()
    data={'status':'success'}
    return JsonResponse(data)

def wishlist_main(request):
    id=request.session['id']
    user_id=User.objects.get(id=id)
    wishlist=wishlist_item.objects.filter(uid=user_id)
    if request.session.get('id',None):
        id=request.session['id']
        addtocart=Add_to_cart.objects.filter(uid=id).all()
        count=Add_to_cart.objects.filter(uid=id).count()
        total=0
        for a in addtocart:
            total+=a.qty*a.pid.products_price
    else:
        total=0
        count=0
    return render(request,'app/wishlist.html',{'wishlist':wishlist,'total':total,'count':count})

def wish_remove(request):
    id=request.GET['id']
    wishlist_item.objects.filter(id=id).delete()
    data={'status':'success'}
    return JsonResponse(data)

def my_order(request):
    id=request.session['id']
    po=placed_order.objects.filter(uid=id).order_by('payment_request_id').values('payment_request_id').distinct()
    if request.session.get('id',None):
        id=request.session['id']
        addtocart=Add_to_cart.objects.filter(uid=id).all()
        count=Add_to_cart.objects.filter(uid=id).count()
        total=0
        for a in addtocart:
            total+=a.qty*a.pid.products_price
    else:
        total=0
        count=0
    
    return render(request,'app/my_order.html',{'place_order':po,'wishlist':wishlist,'addtocart':addtocart,'total':total,'count':count})

def place_oredr_details(request,id):
    uid=request.session['id']
    po=placed_order.objects.filter(uid=uid).filter(payment_request_id=id)
    total_amount=0
    for a in po:
        total_amount+=a.qty*a.pid.products_price

    if request.session.get('id',None):
        id=request.session['id']
        addtocart=Add_to_cart.objects.filter(uid=id).all()
        count=Add_to_cart.objects.filter(uid=id).count()
        total=0
        for a in addtocart:
            total+=a.qty*a.pid.products_price
    else:
        total=0
        count=0
    return render(request,'app/my_order_details.html',{'place_order':po,'wishlist':wishlist,'addtocart':addtocart,'total_amount':total_amount,'total':total,'count':count})