from django.db import models

# Create your models here.
class Messagepost(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to='post_images')