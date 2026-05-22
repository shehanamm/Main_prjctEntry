from django.urls import path
from.views import*
from django.conf import settings
from django.conf.urls.static import static
app_name='petoperation'
urlpatterns = [
    path('addbreed',add_newbreed,name='addnewbreed'),
    path('addpet/',add_pet_donate,name='addpet'),
    path('allpet/',allpets_view,name='allpets_view'),
    path('updatepet/<int:id>',update_petdetails,name='update_petdetails'),
    path('deletepet/<int:id>',delete_pet,name='delete_pet'),
    path('viewpet',view_pet,name='view_pet'),
    path('bookpet/<int:id>',booking,name='pet_booking'),
    path('viewbook/<int:id>',booked_petview,name='booked_petview'),    
    path('cancelpet/<int:id>',cancel_booking,name='cancel_booking'),
    path('petselect/<int:id>',view_allpet,name="view_allpet"),
    path('chat/<int:booking_id>/',chat_msg,name='chat_msg'),
    path('start-chat/<int:pet_id>/', start_chat, name='start_chat'),
    path('allpetsadmin',allpets_admin,name='allpets_admin'),
    path('deleteadmin/<int:id>',delete_pet_admin,name="delete_pet_admin"),
    path('updatepetadmin/<int:id>',updatepetadmin,name='updatepetadmin'),
    path('announcement',post_announcement,name='post_announcement'),

    
]
