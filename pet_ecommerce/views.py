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
  if request.user.role not in ['admin', 'staff']:
   return redirect('Error')
  proedit=get_object_or_404(Product,id=id)
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
  if request.user.role not in ['admin', 'staff']:
   return redirect('Error')
  prodel=Product.objects.get(id=id)
  if request.method == 'POST':
    prodel.delete()
    return redirect('view_allproduct')
  return render(request,'deleteprod.html',{'prodel':prodel})
# @login_required(login_url='/accounts/login')
# def user_addcart_product(request, pro_id):
#  if request.user.role not in ['user', 'donor']:
#    return redirect('Error')
#  product=get_object_or_404(Product,id=pro_id)
#  quantity = int(request.POST.get('quantity', 1))
 
#  if quantity < 1:
#         quantity = 1
#  cart, created = Cart.objects.get_or_create(user=request.user)
#  cart_item, item_created = Cart_item.objects.get_or_create(
#         cart=cart,
#         product=product,
#         defaults={'quantity':quantity}
#     )
#  if not item_created:
#         cart_item.quantity=quantity
#         cart_item.save()

#  return redirect('user_cart')



@login_required(login_url='/accounts/login')
def user_addcart_product(request, pro_id):

    if request.user.role not in ['user', 'donor']:
        return redirect('Error')

    product = get_object_or_404(Product, id=pro_id)

    quantity = int(request.POST.get('quantity', 1))

    if quantity < 1:
        quantity = 1

    cart, _ = Cart.objects.get_or_create(user=request.user)

    # 🔥 FORCE SINGLE ROW PER PRODUCT
    cart_item = Cart_item.objects.filter(cart=cart, product=product).first()

    if cart_item:
        cart_item.quantity = quantity   # overwrite always
        cart_item.save()
    else:
        Cart_item.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    return redirect('user_cart')
@login_required(login_url='/accounts/login')
def user_cart(request):
  if request.user.role not in ['user', 'donor']:
   return redirect('Error')
  
  user_cart,created=Cart.objects.get_or_create(user=request.user)
  cart_items = user_cart.items.select_related('product')

  grand_total = sum(item.quantity * item.product.price for item in cart_items)

    
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
  if request.user.role not in ['admin', 'staff']:
   return redirect('Error')
  prod=Product.objects.get(id=id)
  return render(request,'viewstaff.html',{'prod':prod})

def allprohome(request):
  allobj=Product.objects.all()
  return render(request,'petshop.html',{'allobj':allobj})

@login_required(login_url='/accounts/login')
def order_placed(request):
    cart = get_object_or_404(Cart, user=request.user)
    # insufficient_stock = False  # Flag to track stock issues

    for item in cart.items.all():
        print(item.product.name, item.quantity)
        product = item.product
        if product.stock >= item.quantity:
            product.stock -= item.quantity
            product.save()
        else:
            # insufficient_stock = True
            messages.error(request, f"Not enough stock for {product.name}")

    # if not insufficient_stock:
        
    #     cart.items.all().delete()  # Clear the cart after successful order

    return redirect('user_cart')
def update_cart(request, item_id):
    item = get_object_or_404(Cart_item, id=item_id)

    if request.method == "POST":
        quantity = request.POST.get("quantity", 1)

        try:
            quantity = int(quantity)
        except:
            quantity = 1

        if quantity < 1:
            quantity = 1

        item.quantity = quantity
        item.save()

        messages.success(request, "Cart updated successfully")

    return redirect('user_cart')