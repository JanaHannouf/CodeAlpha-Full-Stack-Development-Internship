from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import mark_safe
from django.db.models.signals import post_save

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=100)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200)
    image = models.ImageField(upload_to="profile-image")

    def profile_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50" />' % (self.image))

    def __str__(self):
        return f"{self.user.username} - {self.full_name} - {self.email}"
    
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)

class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, blank=True, null=True)
    subject = models.CharField(max_length=200, blank=True, null=True)
    message = models.TextField(max_length=200, blank=True, null=True)

    class Meta:
        verbose_name = "Contact Us"
        verbose_name_plural = "Contact Us"

    def __str__(self):
        return self.full_name