from django.db import models
from accounts.models import CustomUser
# Create your models here
class Category_product(models.Model):
    name=models.CharField(max_length=20)
    image=models.ImageField(upload_to='catgory_shop')
    def __str__(self):
        return self.name
class Product(models.Model):
    user = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE)
    name=models.CharField(max_length=25)
    price=models.FloatField()
    img = models.ImageField(upload_to='products')
    cat = models.ForeignKey(Category_product,on_delete=models.CASCADE,null=True)
    stock=models.IntegerField()
    size=models.IntegerField()

    pro_desc=models.TextField(blank=True)
    def __str__(self):
        return self.name
class Cart(models.Model):
    user=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
class Cart_item(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity=models.PositiveIntegerField(default=1)
    def __str__(self):
        return self.product.name
    @property
    def total_price(self):
        return self.quantity * self.product.price
