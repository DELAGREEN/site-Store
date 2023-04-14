from django.db import models
from users.models import User

class ProductCategory(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


    def __str__(self):
        return f'Категория: {self.name}'


class Product(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField(default=0)
    image = models.ImageField(upload_to='products_images')
    category = models.ForeignKey(to=ProductCategory, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


    def __str__(self):
        return f'Продукт: {self.name} | Категория: {self.category.name}'
    

class BasketQuerySet(models.QuerySet):
    
    def total_sum(self):
        #baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in self)
    
    def total_quantity(self):
        #baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in self)


class Basket(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE )
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BasketQuerySet.as_manager()

    def __str__(self):
        return f'Корзина для {self.user.username} | {self.user.email} | Продукт: {self.product.name}'
    

    def sum(self):
        return self.product.price * self.quantity
    


#    total_sum' : total_sum,
#               'total_quantity' : total_quantity


#region important
def total_sum(self):
    baskets = Basket.objects.filter(user=self.user)
    return sum(basket.sum() for basket in baskets)

def total_quantity(self):
    baskets = Basket.objects.filter(user=self.user)
    return sum(basket.quantity for basket in baskets)

#endregion