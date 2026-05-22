from django.contrib import admin

# Register your models here.
from.models import*
admin.site.register(Category)
admin.site.register(Breed)
admin.site.register(Pet)
admin.site.register(Booking)
admin.site.register(ChatMessage)
admin.site.register(Announcement)
