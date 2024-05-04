from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4

# Create your models here.

#custormers
class Customer(models.Model):
    GOLD_MEMBERSHIP = 'G'
    SILVER_MEMBERSHIP = 'S'
    BRONZE_MEMBERSHIP = 'B'
    
    MEMBERSHIP_CHOICES = [
        (GOLD_MEMBERSHIP,'GOLD'),
        (SILVER_MEMBERSHIP,'SILVER'), 
        (BRONZE_MEMBERSHIP,'BRONZE'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone  = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES , default= BRONZE_MEMBERSHIP)
    
    #creating indexes on first_name and last_name
    class Meta:
        indexes = [
            models.Index(fields=['first_name','last_name'])
        ] 
        
    def __str__(self):
        return  f'{self.first_name} {self.last_name}' 
    
    
#category
class Category(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product' , on_delete=models.SET_NULL  ,related_name='+' ,null= True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title
        
    

#promotions
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
    
    
#products
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(null=True , blank=True)
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(1 , message="make sure that the value is grater then 0")]
                                     ) 
    inventory = models.IntegerField(
        validators=[MinValueValidator(1 , message="make sure that the value is grater then 0")]
        )
    last_update = models.DateTimeField(auto_now=True) 
    category = models.ForeignKey(Category , on_delete=models.PROTECT , related_name='products')
    promotion = models.ManyToManyField(Promotion , blank=True)
    
    class Meta:
        ordering = ['title']
    
    def __str__(self):
        return self.title


#orders 
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING,'pending'),
        (PAYMENT_STATUS_COMPLETED,'completed'),
        (PAYMENT_STATUS_FAILED,'failed')
    ]    
    
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1,choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_STATUS_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)
    
        
        

#address
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)    

#order items 
class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitems')
    item_quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

    
    
#cart
class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default= uuid4 )
    created_at = models.DateTimeField(auto_now_add=True)
    


#cart items
class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE , related_name='items')
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveBigIntegerField(
        validators=[MinValueValidator(1)]
    )    
    
    class Meta:
        unique_together = [['cart', 'product']]
    
    

class Reviews(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='reviews')   
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)   
        
    

    

    