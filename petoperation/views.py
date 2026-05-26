from django.shortcuts import render,redirect,get_object_or_404
from.models import Category,Breed,Pet,Booking,ChatMessage,Announcement
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from.forms import Breed_form,Pet_addform,Pet_bookingform,ChatMessageForm,AnnouncementForm
from accounts.utils import Error
# admindashboard,dashboard,donordashboard,userdashboard
# Create your views here.

@login_required(login_url='/accounts/login')
def add_newbreed(requset):
  if not requset.user.is_superuser:
        return redirect('Error')  
  if requset.method=='POST':
      form=Breed_form(requset.POST,requset.FILES)
      if form.is_valid():
        cat= form.save(commit=False)
        cat.save()
        return redirect('admindashboard')
  else:
     form=Breed_form()
     return render(requset,'addbreed.html',{'form':form})
  
@login_required(login_url='/accounts/login')
def add_pet_donate(request):
    if request.user.role!='donor': 
       return redirect("Error")
    form=Pet_addform()
    breeds=Breed.objects.all()
    if request.method=="POST":
      form= Pet_addform(request.POST,request.FILES)
      if form.is_valid():
       pet=form.save(commit=False)
       pet.user=request.user
       pet.save()
      if request.user.role == 'donor':
            return redirect('donordashboard')
      return redirect('userdashboard')
    else:
         form=Pet_addform()
    return render(request,'addpet.html',{'form':form,'breeds':breeds})
def allpets_view(request):
   pets=Pet.objects.all()
   return render(request,'allpets.html',{'pets':pets})
@login_required(login_url='/accounts/login')
def update_petdetails(request,id):
   if request.user.role!='donor':
    return redirect("Error")
   pet=Pet.objects.get(id=id,user=request.user)
   if request.method=='POST':
      form= Pet_addform(request.POST,request.FILES,instance=pet)
      if form.is_valid():
       form.save()
       return redirect('donordashboard')
   else:
        form=Pet_addform(instance=pet)
   return render(request,'editpet.html',{'form':form})
@login_required(login_url='/accounts/login')     
def delete_pet(request,id):
   pet = Pet.objects.get(id=id,user=request.user)
   pet.delete()
   return redirect('allpets_view')
@login_required(login_url='/accounts/login')
def view_pet(request):
   pet = Pet.objects.filter(user=request.user)
   return render(request,'view_pet.html',{'pet':pet})

# booking area
@login_required(login_url='/accounts/login')
def booking(request,id):
   pet=get_object_or_404(Pet,id=id)
   if request.user.role=='donor':
      return redirect('Error')
   if pet.status == 'adopted':
        messages.error(request, "This pet is already adopted.")
        return redirect('allpets_view')

   already_booked= Booking.objects.filter(user=request.user,pet=pet).exists()
   if already_booked:
        messages.warning(request, "You already booked this pet.")
        return redirect('userdashboard')
   if request.method=='POST': 
      # books=Booking.objects.filter(user=request.user)
      form=Pet_bookingform(request.POST)
      if form.is_valid():
         if not already_booked:
            book=form.save(commit=False)
            book.user=request.user
            book.pet=pet
            book.status='pending'
            book.save()   
            return redirect('userdashboard')
      else:
        print(form.errors)
   else:
      form=Pet_bookingform()
     
   return render(request,'petbooking.html',{'form':form,'pet':pet})

def cancel_booking(request,id):

   booking=get_object_or_404(Booking,user=request.user,id=id)
   if booking.status=='pending':
      booking.status='cancelled'
      booking.save()
      messages.success(request,"your order is cancelled")
      return redirect('userdashboard')
@login_required(login_url='/accounts/login')
def booked_petview(request,id):
   booked=get_object_or_404(Booking,user=request.user,id=id)
   return render(request,'bookedpet.html',{'booked':booked})
def view_allpet(request,id):
   pet_selected=get_object_or_404(Pet,id=id) 
   return render(request,'pet_selected.html',{'pet_selected':pet_selected})
# chat area
@login_required(login_url='/accounts/login')
def chat_msg(request,booking_id):
   if request.user.role=='staff':
      return redirect('Error')
   booking=get_object_or_404(Booking,id=booking_id)
   #  booking=Booking.objects.filter(user=request.user,pet=pet)
   if request.user != booking.user and request.user != booking.pet.user:
        return redirect('home')
   
   if request.method=='POST':
      content=request.POST.get('content','').strip()
      if content:
         ChatMessage.objects.create(
                booking=booking,
                sender=request.user,
                content=content
            )
      return redirect('petoperation:chat_msg',booking_id=booking.id)
   chat_messages = booking.messages.order_by('timestamp')
   if chat_messages is not None:
    chat_messages.exclude(sender=request.user).update(is_read=True)

   context = {
        'booking': booking,
        'chat_messages': chat_messages,
        'pet': booking.pet
    }
   return render(request, 'chat_msg.html', context)


def start_chat(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id)
    if pet.user == request.user:
        # Maybe send a message or just redirect home
        return redirect('home')
    booking,created = Booking.objects.get_or_create(
        pet=pet,
        user=request.user,
        defaults={'message_to_donor': "I am interested in adopting this pet."}
    )
    return redirect('petoperation:chat_msg', booking_id=booking.id)


@login_required(login_url='/accounts/login')     
def delete_pet_admin(request,id):
   if not request.user.is_superuser:
    return redirect("Error")
   pet = Pet.objects.get(id=id)
   pet.delete()
   return redirect('admindashboard')
@login_required(login_url='/accounts/login')
def updatepetadmin(request,id):
  
   if not request.user.is_superuser:
    return redirect("Error")
   pet=Pet.objects.get(id=id)
   if request.method=='POST':
      form= Pet_addform(request.POST,request.FILES,instance=pet)
      if form.is_valid():
       form.save()
       return redirect('admindashboard')
   else:
        form=Pet_addform(instance=pet)
   return render(request,'admineditpet.html',{'form':form})
@login_required(login_url='/accounts/login')
def allpets_admin(request):
   if not request.user.is_superuser:
    return redirect("Error")
   all_pets=Pet.objects.all()
   return render(request,'adminallpet.html',{'all_pets':all_pets})
def post_announcement(request):
    if not request.user.is_superuser:
        return redirect('Error') 
    if request.method == 'POST':
        form = AnnouncementForm(request.POST)
        if form.is_valid():
            announcement = form.save(commit=False)
            announcement.posted_by = request.user
            announcement.save()
            print(announcement)
            return redirect('admindashboard') 
    else:
        form = AnnouncementForm()
       
    return render(request, 'announcement.html', {'form': form})    