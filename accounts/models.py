from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('donor', 'Donor'),
        ('user','User')
    )
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default='user')
    is_blocked=models.BooleanField(default=False)
    
class DonorProfile(models.Model):
    name=models.CharField(max_length=50,blank=True)
    address=models.CharField(max_length=100,blank=True)
    age=models.IntegerField(null=True,blank=True)
    city=models.CharField(max_length=30,blank=True)
    phone=models.CharField(max_length=15,blank=True)
    profile_pic=models.ImageField(upload_to='donors',blank=True,null=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
  
    def __str__(self):
        return self.user.username
class UserProfile(models.Model):
    name=models.CharField(max_length=50,blank=True)
    address=models.CharField(max_length=100,blank=True)
    age=models.IntegerField(null=True,blank=True)
    city=models.CharField(max_length=30,blank=True)
    phone=models.CharField(max_length=15,blank=True)
    profile_pic=models.ImageField(upload_to='users',blank=True,null=True)
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.user.username
class StaffProfile(models.Model):
     staff_name=models.CharField(max_length=50,blank=True)
     staff_desg=models.CharField(max_length=50,blank=True)
     profile_pic=models.ImageField(upload_to='staff',blank=True,null=True)
     staff_address=models.CharField(max_length=100)
     staff_dob=models.DateField(null=True,blank=True)
     staff_Location=models.CharField(max_length=30,blank=True)
     staff_contact=models.CharField(max_length=15,blank=True)
     staff_mail=models.EmailField(blank=True)
     user=models.OneToOneField(CustomUser,on_delete=models.CASCADE,default=None)
     def __str__(self):
        return self.user.username
     
class Complaint(models.Model):
   TYPE_CHOICES = (
        ('user', 'User Complaint'),
        ('staff', 'Staff Complaint'),
       ('donor', 'Donor Complaint'),

    )

   type = models.CharField(
        max_length=10,
        choices=TYPE_CHOICES,
        default='user'
    )
   STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('resolved', 'Resolved'),
    )

   user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
   subject = models.CharField(max_length=200)
   message = models.TextField()
   status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
   admin_reply = models.TextField(blank=True, null=True)
   created_at = models.DateTimeField(auto_now_add=True)

   def __str__(self):
            return f"{self.user.username} - {self.subject}"