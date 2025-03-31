from django.db import models
import uuid
from django.utils.timezone import now
from django.contrib.auth.hashers import check_password


class User(models.Model): 
    id = models.IntegerField(primary_key=True, auto_created=True, default=1)  # Auto-incrementing ID
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255) 
    full_name = models.CharField(max_length=255)  
    role = models.CharField(
        max_length=10, 
        choices=[("customer", "Customer"), ("pt", "Personal Trainer"), ("admin", "Admin")], 
        default="customer"
    )
    profile_picture = models.TextField(default="test")  # URL to the profile picture
    created_at = models.DateTimeField(default=now)  # Timestamp when the user was created


    def __str__(self):
        return self.email
    def check_password(self, raw_password):
        return check_password(raw_password, self.password)
    
class Workout(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)  # Duration in minutes
    level = models.CharField(max_length=30, choices=[("beginner", "BEGINNER"), ("intermediate", "INTERMEDIATE"), ("advanced", "ADVANCED")])
    type = models.CharField(max_length=30, choices=[("cardio","CARDIO"), ("strength", "STRENGTH"), ("flexibility", "FLEXIBILITY")])
    isPremium = models.BooleanField(default=False)
    video_url = models.TextField(null=True, blank=True)
    thumbnail_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Subscription(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.CharField(max_length=10, choices=[("monthly", "MONTHLY"), ("yearly", "YEARLY")])
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    payment_status = models.CharField(max_length=10, choices=[("pending", "PENDING"), ("completed", "COMPLETED"), ("failed", "FAILED")])
    created_at = models.DateTimeField(auto_now_add=True)
    
class Gym(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, null=True, blank=True)
    opening_hours = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name    

class GymMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    membership_type = models.CharField(max_length=10, choices=[("monthly", "MONTHLY"), ("yearly", "YEARLY")])
    payment_status = models.CharField(max_length=10, choices=[("pending", "PENDING"), ("completed", "COMPLETED"), ("failed", "FAILED")])
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class PersonalTrainer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="personal_trainer")
    bio = models.TextField(null=True, blank=True)
    experience = models.IntegerField(null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    certification = models.TextField()
    
class PTSession(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pt_sessions")
    trainer = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE, related_name="pt_sessions")
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=10, choices=[("scheduled", "SCHEDULED"), ("completed", "COMPLETED"), ("cancelled", "CANCELLED")])
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Livestream(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    host = models.ForeignKey(PersonalTrainer, on_delete=models.CASCADE, related_name="livestreams")
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    video_url = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=[("upcoming", "UPCOMING"), ("live", "LIVE"), ("ended", "ENDED")])
    created_at = models.DateTimeField(auto_now_add=True)
    participants = models.ManyToManyField(User, related_name="livestreams", blank=True)
    def __str__(self):
        return self.title

class EcommerceProduct(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField()
    image_url = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=10, choices=[("pending", "PENDING"), ("completed", "COMPLETED"), ("failed", "FAILED")]
    )
    created_at = models.DateTimeField(auto_now_add=True)


# 🔟+1 Order Items - Chi tiết đơn hàng
class OrderItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(EcommerceProduct, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

