from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.timezone import now


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient')
    full_name = models.CharField(max_length=200)
    email= models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile_images/', default='medias/account.png', null=True, blank=True)
    joined_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.full_name

# Signal to create or update Patient profile
@receiver(post_save, sender=User)
def create_or_update_patient(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'patient'):
        Patient.objects.create(user=instance)
    else:
        instance.patient.save()


class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialization = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username 
    
class Appointment(models.Model):
    patient_name = models.CharField(max_length=200)
    patient_email = models.EmailField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=20, default="Pending")  # Pending, Approved, or Declined

    def __str__(self):
        return f"Appointment with {self.doctor.user.username} on {self.appointment_date}"