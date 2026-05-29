from django.contrib import admin
from.models import *
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(DonorProfile)
admin.site.register(StaffProfile)



@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('user__username', 'subject')