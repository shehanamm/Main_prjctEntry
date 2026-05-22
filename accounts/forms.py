from django import forms
from.models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from.models import DonorProfile,UserProfile,StaffProfile
class Reguser(UserCreationForm):
    class Meta:
        model=CustomUser
        fields=['username','email']
class DonorProfileForm(forms.ModelForm):
    class Meta:
        model = DonorProfile
        fields = ['name','address', 'age', 'city', 'phone', 'profile_pic']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name','address', 'age', 'city', 'phone', 'profile_pic']
class StaffProfileForm(forms.ModelForm):
    class Meta:
        model=StaffProfile
        exclude=['user']
        widgets = {
            'staff_dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }