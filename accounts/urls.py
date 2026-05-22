from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .views import *
urlpatterns = [
 path('',home,name='home'),
 path('login/',loginpage,name='login'),

 path('register',User_register,name='user_register'),
 path('donorreg',Donor_register,name='donor_register'),
 path('staffreg',staff_register,name='staff_register'),
 path('dashboard',dashboard,name='dashboard'),
 path('userdash',userdashboard,name='userdashboard'),
 path('donordash',donordashboard,name='donordashboard'),
 path('staffdash',staffdashboard,name="staffdashboard"),
 path('admindash',admindashboard,name="admindashboard"),
 path('userprofile',update_user_profile,name="update_user_profile"),
 path('donorprofile',update_donor_profile,name="update_donor_profile"),
 path('staffuodatepro',update_staff_profile,name='update_staff_profile'),
 path('logout',auth_views.LogoutView.as_view(),name='logout'),
 path('login',loginpage),
 path('error',Error,name='Error'),
 path('allusers',all_users,name='all_users'),
 path('useradminedit/<int:id>',user_adminedit,name='user_adminedit'),
 path('donoradminedit/<int:id>',donor_adminedit,name='donor_adminedit'),
 path('staffadminedit/<int:id>',staff_adminedit,name='staff_adminedit'),
 path('viewuseradmin/<int:id>',view_user_admin,name='view_user_admin'),
 path('viewdonoradmin/<int:id>',view_donor_admin,name='view_donor_admin'),
 path('viewstaffadmin/<int:id>/',view_staff_admin,name='view_staff_admin'),
 
 path('deleteuseradmin/<int:id>',user_deleteadmin,name='user_deleteadmin'),
 path('deletedonoradmin/<int:id>',donor_deleteadmin,name='donor_deleteadmin'),
 path('deletestaffadmin/<int:id>',staff_deleteadmin,name='staff_deleteadmin'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)