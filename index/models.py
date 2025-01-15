from django.db import models
from django.forms import ValidationError
from django.utils import timezone

# Create your models here.

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=100, unique=True)
    password = models.CharField(max_length=255)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name} '
    
class Item(models.Model):
    item_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True, null=True)
    condition = models.CharField(
        max_length=15,
        choices=[
            ('New', 'New'),
            ('Used', 'Used'),
            ('Like New', 'Like New'),
            ('Refurbished', 'Refurbished')
        ],
        blank=True,
        null=True
    )
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    rating =models.DecimalField(max_digits=10, decimal_places=2 ,blank=True, null= True) 
    
    def __str__(self):
        return self.title
    
class Transaction(models.Model):
    transaction_id = models.AutoField(primary_key=True)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    buyer = models.ForeignKey('User', related_name='purchases', on_delete=models.CASCADE)
    seller = models.ForeignKey('User', related_name='sales', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(default=timezone.now)
    amount = models.IntegerField()
    code_deliver = models.IntegerField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[
            ('Pending', 'Pending'),
            ('Completed', 'Completed'),
            ('Cancelled', 'Cancelled')
        ],
        default='Pending'
    )

    def __str__(self):
        return f'Transaction {self.transaction_id} - {self.item.title}'

class ItemStatus(models.Model):
    itemStatus_id = models.AutoField(primary_key=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    added_to_cart = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    def __str__(self):
        return f'itemStatus {self.itemStatus_id} - {self.item.title}'

class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    transaction = models.ForeignKey('Transaction', on_delete=models.CASCADE)
    reviewer = models.ForeignKey('User', on_delete=models.CASCADE)
    rating = models.IntegerField()
    review_text = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Review {self.review_id} - {self.transaction.item.title}'

    def clean(self):
        if self.rating < 1 or self.rating > 5:
            raise ValidationError('Rating must be between 1 and 5.')







