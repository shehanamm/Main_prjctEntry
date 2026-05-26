from django.urls import path
from.views import*
from django.conf import settings
from django.conf.urls.static import static
urlpatterns=[
    path('addproduct',add_product,name='add_product'),
    path('view_allpro',view_allproduct,name="view_allproduct"),
    path('editpro/<int:id>',edit_product,name='edit_product'),
    path('prodetails/<int:id>',one_product_details,name='one_product_details'),
    path('deletepro/<int:id>',delete_product,name='delete_product'),
    path('useraddcart/<int:pro_id>',user_addcart_product,name='addcart'),
    path('usercart',user_cart,name='user_cart'),
    path('removecart/<int:id>',cart_item_remove,name="cart_item_remove"),
    path('viewstaff/<int:id>',staff_view,name="staff_view"),
    path('allprohome',allprohome,name="allhome"),
    path('order_placed',order_placed,name='order_placed'),
    path('cart/update/<int:item_id>/',update_cart, name='update_cart'),
    
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)