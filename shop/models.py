from django.db import models

# Create your models here.
class ProductImage(models.Model):
    image = models.ImageField()

    def __str__(self):
        return str(self.image)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(blank=True, null=True)
    images = models.ManyToManyField(ProductImage, related_name='images', blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='products', on_delete=models.CASCADE)

    def __str__(self):
        return str(self.name)