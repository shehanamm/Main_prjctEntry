from django import forms
from.models import Category,Breed,Pet,Booking,Announcement
 
class Category_form(forms.ModelForm):
    class Meta:
        model=Category
        fields='__all__'
class Breed_form(forms.ModelForm):
    class Meta:
        model=Breed
        fields='__all__'
class Pet_addform(forms.ModelForm):
    class Meta:
        model=Pet
        exclude=['user','status','posted_date']
class Pet_bookingform(forms.ModelForm):
    class Meta:
        model=Booking
        exclude=['user', 'pet', 'status', 'applied_at', 'message_to_donor']
from django import forms
from .models import ChatMessage

class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['content']
        widgets = {
            'content': forms.TextInput(attrs={
                'placeholder': 'Type your message...',
                'class': 'form-control chat-input',
                'autocomplete': 'off'
            }),
        }

from .models import Announcement

class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ['title', 'message', 'is_active','start_date','end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }