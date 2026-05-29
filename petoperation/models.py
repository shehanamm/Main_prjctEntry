from django.db import models
from accounts.models import CustomUser
# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=50)
    image=models.ImageField(upload_to='petcategory')
    def __str__(self):
        return self.name
class Breed(models.Model):
    cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    breed_name=models.CharField(max_length=30)
    def __str__(self):
        return self.breed_name
class Pet(models.Model):
    pet_name=models.CharField(max_length=30)
    pet_img=models.ImageField(upload_to='don_petimg')
    pet_cat=models.ForeignKey(Category,on_delete=models.CASCADE)
    pet_breed=models.ForeignKey(Breed,on_delete=models.CASCADE)
    pet_age=models.IntegerField()
    price=models.FloatField(blank=True,null=True)
    pet_location=models.CharField(max_length=50)
    pet_vaccinated=models.BooleanField(default=False)
    pet_desc=models.TextField()
    pet_reason=models.CharField(max_length=100)
    posted_date=models.DateTimeField(auto_now_add=True)
    status=models.CharField(max_length=50,choices=(('available','Available'),('adopted','Adopted')),
                            default='available')
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    def __str__(self):
        return self.pet_name
class Booking(models.Model):
    STATUS_CHOICES=(('pending','pending'),
                   ('approved','Approved'),
                   ('rejected','Rejected'),
                    ('cancelled','Cancelled'))
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='my_bookings')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    message_to_donor = models.TextField(blank=True, help_text="Why do you want to adopt?")

    class Meta:
        ordering = ['applied_at'] 
    def __str__(self):
        return f"{self.user.username} booked {self.pet.pet_name}"

class ChatMessage(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read=models.BooleanField(default=False)

    class Meta:
        ordering = ['timestamp']
    def __str__(self):
        return f"{self.sender.username} - {self.booking.pet.pet_name}"
class Announcement(models.Model):
    title=models.CharField(max_length=100)
    message = models.TextField()
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)

    posted_by = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title


class DonorRating(models.Model):

    donor = models.ForeignKey(
       CustomUser,
        on_delete=models.CASCADE,
        related_name='received_ratings'
    )

    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='given_ratings'
    )

    booking = models.ForeignKey(
        'Booking',
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    review = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'booking')  # prevent multiple ratings

    def __str__(self):
        return f"{self.user} → {self.donor} ({self.rating})"


class SystemRating(models.Model):

    user = models.ForeignKey(
            CustomUser,
        on_delete=models.CASCADE
    )

    rating = models.IntegerField()

    review = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.rating}"
class Notification_donor(models.Model):
        user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
        message = models.TextField()
        created_at = models.DateTimeField(auto_now_add=True)
        is_read = models.BooleanField(default=False)