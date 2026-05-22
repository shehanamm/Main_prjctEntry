from django.shortcuts import render,redirect,get_object_or_404
from.models import Product,Cart_item,Cart
from.forms import Product_form
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from accounts.utils import Error
# # Create your views here.
@login_required(login_url='/accounts/login')
def add_product(request):
 if request.user.role not in ['staff', 'admin']:
   return redirect('Error')
 if request.method=='POST':
  form=Product_form(request.POST,request.FILES)
  if form.is_valid() :
     product = form.save(commit=False)
     product.user = request.user
     product.save()
     return redirect('staffdashboard')
 else:
   form=Product_form()
   return render(request,'product.html',{'form':form})
 
def view_allproduct(request):
  allpro=Product.objects.all()
  return render(request,'allproduct.html',{'allpro':allpro})
@login_required(login_url='/accounts/login')
def edit_product(request,id):
   if request.user.role!='staff':
    return redirect('Error')
   proedit=Product.objects.get(user=request.user,id=id)

   if request.method=='POST':
     form=Product_form(request.POST,request.FILES,instance=proedit)
     if form.is_valid():
       form.save()
     return redirect('view_allproduct')
   else:
     form=Product_form(instance=proedit)
     return render(request,'editproduct.html',{'form':form})

def one_product_details(request,id):
  pro=Product.objects.get(id=id)
  return render(request,'detailpro.html',{'pro':pro})
@login_required(login_url='/accounts/login')
def delete_product(request,id):
  prodel=Product.objects.get(id=id)
  if request.method == 'POST':
    prodel.delete()
    return redirect('view_allproduct')
  return render(request,'deleteprod.html',{'prodel':prodel})
@login_required(login_url='/accounts/login')
def user_addcart_product(request,pro_id):
  if request.user.role not in ['user', 'donor']:
   return redirect('Error')

  product=get_object_or_404(Product,id=pro_id)
  quantity = int(request.POST.get('quantity', 1))
  if quantity < 1:
        quantity = 1
  cart, created = Cart.objects.get_or_create(user=request.user)
  cart_item, item_created = Cart_item.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity':quantity}
    )
  if not item_created:
        cart_item.quantity=quantity
        cart_item.save()

  return redirect('user_cart')
@login_required(login_url='/accounts/login')
def user_cart(request):
  if request.user.role not in ['user', 'donor']:
   return redirect('Error')

  user_cart,created=Cart.objects.get_or_create(user=request.user)
  cart_items=user_cart.items.all()
  grand_total=sum(item.total_price() for item in cart_items)
  context= {
            'cart_items': cart_items,
            'grand_total': grand_total
    
    }
  return render(request,'cart.html',context)
def cart_item_remove(request,id):
    item = Cart_item.objects.get(id=id, cart__user=request.user)
    item.delete()
    return redirect('user_cart')
@login_required(login_url='/accounts/login')
def staff_view(request,id):
  if request.user.role!='staff':
    return redirect('Error')
  prod=Product.objects.get(id=id)
  return render(request,'viewstaff.html',{'prod':prod})

def allprohome(request):
  allobj=Product.objects.all()
  return render(request,'petshop.html',{'allobj':allobj})
def order_placed(request):
  cart=get_object_or_404(Cart,user=request.user)
  for item in cart.items.all():
    product=item.product
    if product.stock >= item.quantity:
       product.stock -=item.quantity
       product.save()
      
    else:
          messages.error(request, f"Not enough stock for {product.name}")
    return redirect('user_cart')
