from django.db import models

# Create your models here.
class Customer(models.Model):
    customer_name = models.CharField(max_length=150)
    customer_username = models.CharField(max_length=50, unique=True)
    customer_pass = models.CharField(max_length=50)

class Messagepost(models.Model):
    message = models.TextField()
    message_image = models.ImageField(upload_to='images/materials/', null=True, blank=True)
    message_posting_time = models.DateTimeField(auto_now_add=True)
    message_customer = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        ordering = ["message_customer", "message_posting_time"]

class Products(models.Model):
    product_id = models.CharField(max_length=20, primary_key=True)
    product_name = models.CharField(max_length=150)
    product_color = models.CharField(max_length=50)
    product_material = models.CharField(max_length=200)
    product_material_advantage = models.TextField()



