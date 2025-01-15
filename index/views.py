from django.forms import ValidationError
from django.utils import timezone
from django.shortcuts import render, redirect ,get_object_or_404
from .models import Item, Transaction, ItemStatus ,Review
from .forms import User_form, Item_form, LoginForm, ItemStatus_form ,ReviewForm ,TransactionForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .utils import get_login_user,is_get_vilad , get_rating
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def account(request):
    context = {}
    return render(request, "index/account.html", context)

def welcome(request):
    user = get_login_user(request)
    context = {'user':user}
    return render(request, "index/welcome.html", context)

def index(request):
    user = get_login_user(request)
    queries_or =Q()
    queries_and =Q()
    price = None
    search_query = request.GET.get('search', '').strip()
    adviser = True
    if search_query:
        adviser = False
        # Perform search using case-insensitive filtering
        queries_or |= Q(title__icontains=search_query) 
        queries_or |= Q(description__icontains=search_query)
    if request.method =='POST':
        adviser = False
        sort_by_price = request.POST.get('sort_by_price',None)
        condition = request.POST.get('condition',None)
        rating = request.POST.get('rating',None)
        category = request.POST.get('category',None)
        if sort_by_price:
            if sort_by_price =='desc':
                price='-price'
            else:
                price='price'
        if condition:
            queries_and &= Q(condition__icontains=condition)
        if rating:
             queries_and &= Q(rating__gte=rating)
        if category:
             queries_and &= Q(category__icontains=category)

    if price:
        items = Item.objects.exclude(user=user).filter(queries_and).filter(queries_or).order_by(price)
    else:
        items = Item.objects.exclude(user=user).filter(queries_and).filter(queries_or)
    
    

                      
    context = {'items': items , 'adviser':adviser}
    return render(request, "index/index.html", context)

def cart(request):
    user = get_login_user(request)
    item_statuses = ItemStatus.objects.filter(user=user,added_to_cart= True )
    carts = ItemStatus.objects.filter(user=user, added_to_cart=True)
    message=None
    total_price =0
    for item_status in item_statuses:
        total_price+= item_status.item.price

    
    if request.method == 'POST':
        purchase =request.POST.get('purchase', None)
        cancel =request.POST.get('cancel', None) 
        if purchase == 'purchase':
            for item_status in item_statuses:
                print(item_status)
                transaction_data ={
                    'item':item_status.item,
                    'buyer':user,
                    'seller':item_status.item.user,
                    'transaction_date' : timezone.now(),
                    'amount' : 1,
                    'code_deliver' :1234,
                    'status':'Pending',
                }
                form = TransactionForm(transaction_data)
                if form.is_valid():
                    form.save()

                item_status.added_to_cart =False
                item_status.save()
            message='successful'    
            #return redirect('transaction')
        elif cancel == 'cancel':
            for item_status in item_statuses:
                item_status.added_to_cart =False
                item_status.save()
            return redirect('cart')
    

    context = {'item_statuses': item_statuses , 'total_price':total_price , 'carts':carts , 'message':message }
    return render(request, "index/cart.html", context)

def display_personal_information(request):
    user = get_login_user(request)
    context = {'user':user }
    return render(request, "index/display_personal_information.html", context)

def favourite(request):
    user = get_login_user(request)
    item_statuses = ItemStatus.objects.filter(user=user, favorite=True)
    context = {'item_statuses': item_statuses}
    return render(request, "index/favourite.html", context)

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  # Redirect to home page or other view
            else:
                messages.error(request, 'Invalid username or password')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, "index/login.html", context)

def user_register(request):
    if request.method == 'POST':
        form = User_form(request.POST, request.FILES)

        if form.is_valid():
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            admin_user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            # Mark the user as active and staff (can access the admin interface)
            admin_user.is_active = True
            admin_user.is_staff = True
            admin_user.is_superuser = False
            # Save the user
            admin_user.save()
            form.save()
            return redirect('index')
    else:
        form = User_form()

    context = {'form': form}
    return render(request, "index/user_register.html", context)

def item_register(request):
    user = get_login_user(request)
    if request.method == 'POST':
        form = Item_form(request.POST, request.FILES)
        if form.is_valid():
            instance_item = form.save( commit=False)
            instance_item.user = user
            instance_item.save() 
            return redirect('your_item')
    else:
        form = Item_form()    

    context = {'user': user , 'form':form}
    return render(request, "index/item_register.html", context)

def user_logout(request):
    logout(request)  # Logs out the user
    return redirect('index')  # Redirects to the login page after logout

def item_details(request, item_id):
    user = get_login_user(request)
    item = Item.objects.get(item_id=item_id)
    item_status = ItemStatus.objects.filter(item =item_id,user =user)
    if is_get_vilad(item_status):
        item_status = ItemStatus.objects.get(item =item_id,user =user)
    else:
        item_status= None
    reviews=''
    transactions = Transaction.objects.filter(item =item.item_id)
    query = Q()
    for transaction in transactions:
        query |= Q(transaction=transaction)
        reviews = Review.objects.filter(query)
    context = {
                'item': item,
                'user': user ,
                'reviews':reviews,
                'item_status':item_status,
                }

    if request.method == 'POST':
        # delete item status and replece with new status
        print(' pass from here 1')
        if ItemStatus.objects.filter(item =item_id,user =user).exists():
            delete_item_status = ItemStatus.objects.filter(item =item_id,user =user)
            delete_item_status.delete()

        form = ItemStatus_form(request.POST)
        if form.is_valid():
            #check the user do not change front-end code
            instance =form.save(commit=False)
            if  instance.user == get_login_user(request):
                form.save()
                return redirect(request.path)
            else:
                raise ValidationError("You can only register items with your own user ID.")

    return render(request, "index/item_details.html", context)

def transaction(request):
    user = get_login_user(request)
    transactions = Transaction.objects.filter(buyer=user) 
    if request.method == 'POST':
        transaction_id =request.POST['Completed_button']
        if transaction_id :
            transaction= Transaction.objects.get(transaction_id=transaction_id)
            transaction.status = 'Completed'
            transaction.save()

    context = {'transactions': transactions}
    return render(request, "index/transaction.html", context)

def transaction_seller(request):
    massage = None
    user = get_login_user(request)
    transactions = Transaction.objects.filter(seller=user) 
    if request.method == 'POST':
        transaction_id =request.POST.get('Completed_button')
        code_deliver =request.POST.get('code_deliver')
        if transaction_id :
            transaction= Transaction.objects.get(transaction_id=transaction_id)
            if int(transaction.code_deliver)==int(code_deliver):
                transaction.status = 'Completed'
                transaction.save()
            else:
                 massage='The code enter does not match'   


    context = {'transactions': transactions,'massage':massage }
    massage = None
    return render(request, "index/transation_seller.html", context)

def review(request ,transaction_id):
    transaction = Transaction.objects.get(transaction_id =transaction_id )
    review = Review.objects.filter(transaction = transaction_id )
    if is_get_vilad(review):
        review = Review.objects.get(transaction = transaction_id )
    else:
        review= None
    context = {'transaction': transaction , 'review':review }
    if request.method == 'POST':
        delete_review_id= request.POST.get('delete_review')
        if(delete_review_id):
            review = Review.objects.get(review_id = delete_review_id )
            item_id = review.transaction.item.item_id
            review.delete()
            item = Item.objects.get(item_id = item_id)
            item.rating = get_rating(item_id)
            item.save()
        else:
            post_data = request.POST.copy()
            post_data['review_date'] =timezone.now()
            form = ReviewForm(post_data)
            if form.is_valid():
                instance = form.save(commit=False)
                form.save()
                item_id = instance.transaction.item.item_id
                item = Item.objects.get(item_id = item_id)
                item.rating = get_rating(item_id)
                item.save()

                return redirect(request.path)
            else:
                form = ReviewForm()
        return redirect(request.path) # this line of code stop submit from trigger        

           
       
    return render(request, "index/review.html", context)

def your_item(request):
    user = get_login_user(request)
    items = Item.objects.filter(user=user)
    if request.method =='POST':
         item = Item.objects.filter(user=user , item_id =request.POST['delete_item'])
         item.delete()
        

    context = {'items': items}
    return render(request, "index/your_item.html", context)

def update_item(request , item_id):
    user = get_login_user(request)
    item = Item.objects.get(item_id=item_id)
    context = {'item': item , 'user':user}
    if request.method =='POST':
        update_item = get_object_or_404(Item, pk=item_id)
        #delete_item.delete()
        form = Item_form(request.POST ,request.FILES)
        if form.is_valid():


            update_item.title = request.POST.get('title',update_item.title)
            update_item.description =request.POST.get('description',update_item.description)
            update_item.price = request.POST.get('price',update_item.price)
            update_item.category = request.POST.get('category',update_item.category)
            update_item.condition = request.POST.get('condition',update_item.condition)
            update_item.image = request.FILES.get('image',update_item.image)


            update_item.save()

            return redirect('your_item')
                
    return render(request, "index/update_item.html", context)

def update_account(request):
    user = get_login_user(request)
    context = {'user':user}
    if request.method =="POST":
        admin_user = User.objects.get(username=user.username)


        user.username = request.POST.get('username',user.username)
        user.email = request.POST.get('email',user.email)
        user.first_name = request.POST.get('first_name',user.first_name)
        user.middle_name = request.POST.get('middle_name',user.middle_name)
        user.last_name = request.POST.get('last_name',user.last_name)
        user.phone_number = request.POST.get('phone_number', user.phone_number)
        user.image = request.FILES.get('image',user.image)

        user.save()

        admin_user.username=user.username
        admin_user.email=user.email
        admin_user.first_name= user.first_name
        admin_user.middle_name=user.middle_name
        admin_user.last_name=user.last_name

        admin_user.save()

        
        messages.success(request, 'Form update successfully!')

    return render(request, "index/update_account.html", context)

def reset_password(request):
    context = {}
    user = get_login_user(request)
    admin_user = User.objects.get(username=user.username)
    if request.method =="POST":
        old_password= request.POST.get('old_password')
        new_password= request.POST.get('new_password')
        confirm_password= request.POST.get('confirm_password')
        if user.password == old_password and new_password == confirm_password :
             user.password = new_password
             user.save()
             admin_user.set_password(new_password)
             admin_user.save()
             messages.success(request, 'Form reset successfully!')
        else:
             messages.error(request, 'Form reset fail!')

          
        
    return render(request, "index/reset_password.html", context)


    
