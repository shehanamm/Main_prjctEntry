from django.shortcuts import get_object_or_404
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import Reguser,DonorProfileForm,UserProfileForm,StaffProfileForm,ComplaintForm
from.models import CustomUser,DonorProfile,UserProfile,StaffProfile,Complaint
from petoperation.models import Booking,Announcement
from pet_ecommerce.models import Product
from petoperation.views import Pet,ChatMessage,post_announcement
from accounts.utils import Error
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.contrib.sessions.models import Session

# Create your views here.
def home(request):
    now = timezone.now()
    announcements =Announcement.objects.filter(
        is_active=True,
        # start_date__lte=now,
        end_date__gte=now
    ).order_by('-created_at')
    return render(request,'home.html', {'announcements': announcements})

# User Registation--------------

def User_register(request):
    if request.method=='POST':
        form=Reguser(request.POST)
        if form.is_valid():
         user=form.save()
         user.role="user"
         user.save()
         UserProfile.objects.create(user=user)
         login(request,user)
      
         return redirect('dashboard')
       
    else:
        form=Reguser()
    return render(request,'register.html',{'form':form})
def Donor_register(request):
    if request.method=='POST':
        form=Reguser(request.POST)
        if form.is_valid():
            donor=form.save(commit=False)
            donor.role='donor'
            donor.save()
            login(request,donor)
            DonorProfile.objects.create(user=donor)
            return redirect('dashboard')
    else:
         form=Reguser()
    return render(request,'register.html',{'form':form})
def staff_register(request):
    if request.method=='POST':
        form=Reguser(request.POST)
        if form.is_valid():
         user=form.save()
         user.role="staff"
         user.save()
         StaffProfile.objects.create(user=user)
         login(request,user)
         return redirect('dashboard')
    else:
        form=Reguser()
    return render(request,'register.html',{'form':form})
# dashboard area
@login_required    
def dashboard(request):
    if request.user.role=='user':
        return redirect('userdashboard')
    elif request.user.role=='donor':
        return redirect('donordashboard')
    elif request.user.role=='staff':
        return redirect('staffdashboard')
    elif request.user.role=='admin':
        return redirect('admindashboard')
    else:
        return render('Error')
    
# acconts user dashboard------------------
@login_required(login_url='/accounts/login')
def userdashboard(request):
    if request.user.role!='user':
       return redirect('Error')
    else:
    #   usr=CustomUser.objects.filter(role='user')
      pro, created = UserProfile.objects.get_or_create(user=request.user )
      pet_user=Pet.objects.filter(user=request.user)
      my_booking=Booking.objects.filter(user=request.user,).select_related('pet')
    
      user_chat=Booking.objects.filter(user=request.user)
      unread_count = ChatMessage.objects.filter(booking__user=request.user ,is_read=False).exclude(sender=request.user).count()
      complaints = Complaint.objects.filter(user=request.user, type='user').order_by('-created_at')
        
      return render(request,'user.html',{'pro':pro,'pet_user':pet_user,'my_booking':my_booking,'user_chat':user_chat,'unread_count':unread_count,'complaints':complaints})
    
@login_required(login_url='/accounts/login')
def donordashboard(request):
    if request.user.role!='donor':
        return redirect('Error')
    else:
        don=CustomUser.objects.filter(role='donor')
        pro=DonorProfile.objects.get(user=request.user)
        pet_donate=Pet.objects.filter(user=request.user)
        donor_chat=Booking.objects.filter(pet__user=request.user).select_related('user','pet')
        unread_count = ChatMessage.objects.filter(booking__user=request.user, 
        is_read=False).exclude(sender=request.user).count()
        complaints = Complaint.objects.filter(
             user=request.user,
              type='donor'
             ).order_by('-created_at')
    return render(request,'donor.html',{'don':don,'pro':pro,'pet_donate':pet_donate,'donor_chat':donor_chat,'unread_count':unread_count,'complaints':complaints})
    
@login_required(login_url='/accounts/login') 
def admindashboard(request):
    if not request.user.is_superuser:
        return redirect('Error')  
    total_pets=Pet.objects.count()
    # pending_pets=Pet.objects.filter(status='pending').count()
    adopted_pets=Pet.objects.filter(status='adopted').count()
    products=Product.objects.all().order_by('-id')[:5]
    pets=Pet.objects.all().order_by('-id')[:5]
    complaints = Complaint.objects.all().order_by('-created_at')

    return render(request, 'admindash.html',{'pets':pets,'total_pets':total_pets,'adopted_pets':adopted_pets,'products':products,'complaints':complaints})

@login_required(login_url='/accounts/login')
def staffdashboard(request):
    if request.user.role != 'staff':
        return redirect('Error')
    else:
     pro=StaffProfile.objects.get(user=request.user)
     products=Product.objects.all().order_by('-id')[:5]
     complaints = Complaint.objects.filter(type='staff').order_by('-created_at')

     return render(request, 'staffdash.html',{'pro':pro,'products':products,'complaints':complaints})

#loginand logout------------



def loginpage(request):



    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        # STEP 1: authenticate FIRST
        user = authenticate(request, username=username, password=password)

        if user is not None:

            # STEP 2: NOW check block
            if user.is_blocked:
                messages.error(
                    request,
                    "Your account has been blocked by admin. Please contact admin."
                )
                return redirect('login')

            login(request, user)
            return redirect('dashboard')

        # invalid login
        messages.error(request, "Invalid username or password")
        return redirect('login')

    return render(request, 'login.html')

def logoutpage(request):
    logout(request)
    return redirect('home')

@login_required(login_url='/users/login')
def update_user_profile(request):
    if request.user.role!='user':
     return redirect('Error')
    userpro,created = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST,request.FILES,instance=userpro)
        if form.is_valid():
            # data = form.save(commit=False)
            # data.user = request.user
            form.save()
            return redirect(userdashboard)
    else:
        form = UserProfileForm(instance=userpro)
    return render(request, 'updateuserprofile.html', {'form': form})

@login_required(login_url='/users/login')
def update_donor_profile(request):
    if request.user.role!='donor':
     return redirect('Error')
    userpro ,created= DonorProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = DonorProfileForm(request.POST, request.FILES, instance=userpro)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.save()
            return redirect(donordashboard)
    else:
        form =DonorProfileForm(instance=userpro)
    return render(request, 'updatedonorprofile.html', {'form': form})

@login_required(login_url='/users/login')
def update_staff_profile(request):
    if request.user.role !='staff':
     return redirect('Error')
    profile,created= StaffProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = StaffProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # data = form.save(commit=False)
            # data.user = request.user
            form.save()
            return redirect(staffdashboard)
    else:
        form =StaffProfileForm(instance=profile)
    return render(request, 'updatestaffpro.html', {'form': form})

# manage users admin
@login_required(login_url='/users/login')
def staff_adminedit(request,id):
    if request.user.role != 'admin':
     return redirect('Error')
    staff=get_object_or_404(StaffProfile,user__id=id)
    if request.method=='POST':
        form=StaffProfileForm(request.POST,request.FILES,instance=staff)
        if form.is_valid():
            form.save()
            return redirect('admindashboard')
    else:
        form=StaffProfileForm(instance=staff)
    return render(request,'updatestaffpro.html',{'form':form,'staff':staff})
@login_required(login_url='/users/login')
def user_adminedit(request,id):
    if request.user.role != 'admin':
     return redirect('Error')
    user=get_object_or_404(UserProfile,user__id=id)
    if request.method=='POST':
        form=UserProfileForm(request.POST,request.FILES,instance=user)
        if form.is_valid():
            form.save()
            return redirect('admindashboard')
    else:
        form=UserProfileForm(instance=user)
    return render(request,'updateuserprofile.html',{'form':form,'user':user})
@login_required(login_url='/users/login')
def donor_adminedit(request,id):
    if request.user.role != 'admin':
     return redirect('Error')
    donor=get_object_or_404(DonorProfile,user__id=id)
    if request.method=='POST':
        form=DonorProfileForm(request.POST,request.FILES,instance=donor)
        if form.is_valid():
            form.save()
            return redirect('admindashboard')
    else:
        form=DonorProfileForm(instance=donor)
    return render(request,'updatedonorprofile.html',{'form':form,'donor':donor})

@login_required(login_url='/users/login')
def view_user_admin(request,id):

    if request.user.role != 'admin':
     return redirect('Error')

    user = get_object_or_404(UserProfile,user__id=id)

    return render(request,'viewadmin_user.html',{'user':user})
def view_donor_admin(request,id):

    if request.user.role != 'admin':
     return redirect('Error')

    donor= get_object_or_404(DonorProfile,user__id=id)

    return render(request,'viewadmin_donor.html',{'donor':donor})

def view_staff_admin(request, id):
    if request.user.role != 'admin':
        return redirect('Error')

    staff = get_object_or_404(StaffProfile, user__id=id)
    return render(request, 'viewadmin_staff.html', {'staff': staff})
def all_users(request):
    allusers=CustomUser.objects.filter(role__in=["user" ,'donor'])
    allstaff=CustomUser.objects.filter(role='staff')
    return render(request,'allusers.html',{'allusers':allusers,'allstaff':allstaff})

@login_required(login_url='/users/login')
def user_deleteadmin(request,id):
    if request.user.role != 'admin':
     return redirect('Error')
    del_user=get_object_or_404(UserProfile,user__id=id)
    if request.method=='POST':
     del_user.delete()
     return redirect('admindashboard')
@login_required(login_url='/users/login')
def donor_deleteadmin(request,id):
    if request.user.role != 'admin':
     return redirect('Error')
    del_donor=get_object_or_404(DonorProfile,user__id=id)
    if request.method=='POST':
     del_donor.delete()
    return redirect('admindashboard')
@login_required(login_url='/users/login')
def staff_deleteadmin(request,id):
    if request.user.role != 'admin':
     return redirect('Error')
    del_staff=get_object_or_404(CustomUser,id=id)
    if request.method=='POST':
     del_staff.delete()
     return redirect('admindashboard')
@login_required
def admin_block_user(request, id):

    if request.user.role != 'admin':
        return redirect('Error')

    user = get_object_or_404(CustomUser, id=id)

    # Prevent admin blocking themselves
    if user == request.user:
        return redirect('all_users')

    user.is_blocked = not user.is_blocked
    user.save()
    if user.is_blocked:
        active_sessions = Session.objects.filter(expire_date__gte=timezone.now())  
        for session in active_sessions:
            session_data = session.get_decoded()
            if session_data.get('_auth_user_id') == str(user.id):
                session.delete()
    return redirect('all_users')
@login_required
def send_complaint(request):
    if request.method == 'POST':
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.type = 'user'
            complaint.save()
            return redirect('userdashboard')
    else:
        form = ComplaintForm()

    return render(request, 'send_complaint.html', {'form': form})

def reply_complaint(request, id):
    if request.user.role != 'admin':
        return redirect('Error')

    complaint = get_object_or_404(Complaint, id=id)

    if request.method == 'POST':
        complaint.admin_reply = request.POST.get('reply')
        complaint.status = 'reviewed'
        complaint.save()

    return redirect('admindashboard')
@login_required
def staff_send_complaint(request):

    if request.user.role != 'staff':
        return redirect('Error')

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Complaint.objects.create(
            user=request.user,
            subject=subject,
            message=message,
            type='staff'
        )

        return redirect('staffdashboard')

    return render(request, 'send_complaint.html')
@login_required(login_url='/users/login')
def donor_send_complaint(request):
    if request.user.role != 'donor':
        return redirect('Error')

    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        Complaint.objects.create(
            user=request.user,
            subject=subject,
            message=message,
            type='donor',   # IMPORTANT FIX
            status='pending'
        )

        return redirect('donordashboard')

    return render(request, 'send_complaint.html')
@login_required(login_url='/users/login')
def reply_complaint(request, id):
    if request.user.role != 'admin':
        return redirect('Error')

    complaint = get_object_or_404(Complaint, id=id)

    if request.method == 'POST':
        reply = request.POST.get('reply')

        complaint.admin_reply = reply
        complaint.status = 'reviewed'
        complaint.save()

        return redirect('admindashboard')

    return render(request, 'reply_complaint.html', {'complaint': complaint})