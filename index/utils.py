from .models import Transaction ,Review
from django.db.models import Q
from django.db.models.signals import post_delete
from django.dispatch import receiver

def get_login_user(request):
    from .models import User
    if request.user.is_authenticated:
        username = request.user.username
        user = User.objects.get(username=username)
        return user
    else:
        return None
    
   

def is_get_vilad(value: object)-> bool:
    if value.exists() and len(value) == 1:
        return True
    else:
        return False

def get_rating(item_id:int):
    transactions = Transaction.objects.filter(item =item_id)
    if(transactions):
        query = Q()
        for transaction in transactions:
            query |= Q(transaction=transaction)
            reviews = Review.objects.filter(query)  
    else:
        return None          
    
    if(reviews):
        rating_sum =0
        for review in reviews:
            rating_sum +=review.rating

        rating_average = rating_sum/len(reviews)    
    else:
        return None            
    
    return rating_average

def filter_rating(rating:int, items:object)-> list:
    filter_rating =[]
    for item in items:
        check =get_rating(item.item_id)
        if check >=rating:
            filter_rating.append(item)
    return filter_rating      

def calculate_average_rating(item:object):
        item.rating=get_rating(item.item_id)

@receiver(post_delete, sender=Review)
def update_item_rating_on_delete_review(sender, instance, **kwargs):
    item = instance.transaction.item
    if item:
        calculate_average_rating(item)

@receiver(post_delete, sender=Transaction)
def update_item_rating_on_delete_transaction(sender, instance, **kwargs):
    item = instance.item
    if item:
        calculate_average_rating(item)





    
    


