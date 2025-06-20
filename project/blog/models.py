from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager
from taggit.models import Tag
from django.shortcuts import  get_object_or_404 
from django.db.models import Count


# Create your models here.

class Blog(models.Model):
    title = models.CharField( max_length=500)
    content = models.TextField()
    img = models.ImageField( upload_to='blog-image/',)
    date = models.DateField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = TaggableManager()
    
 
   
    def get_absolute_url(self):
        return reverse("detail_blog", kwargs={"pk": self.pk})
    

    def get_related_posts_by_tags(self):
        return Blog.objects.filter(tags__in=self.tags.all()).exclude(id=self.id).distinct()[:4]

    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    comment = models.CharField(max_length=1500)
    user = models.ForeignKey(User, on_delete=models.SET_NULL , null=True)
    active = models.BooleanField(default=False)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment 

class About(models.Model):
    title = models.CharField(max_length=150)
    content = models.TextField()
    img = models.ImageField( upload_to='about/')
    background = models.TextField()
    team = models.TextField(default=None)
    our_core_value = models.TextField()
    

    
    def __str__(self):
        return self.title

