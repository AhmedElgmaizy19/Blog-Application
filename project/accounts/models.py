from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField( max_length=50)
    age = models.IntegerField(default=0,blank=True)
    img = models.ImageField( upload_to='profile-image/',)
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    def get_absolute_url(self):
        return reverse("profile", kwargs={"pk": self.pk})