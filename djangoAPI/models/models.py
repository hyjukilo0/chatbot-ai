from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_username = models.CharField(max_length=50, unique=True)
    customer_pass = models.CharField(max_length=50)

class Messagepost(models.Model):
    message = models.TextField()
    image = models.ImageField(upload_to='post_images')
    posting_time = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

class Products(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True)


