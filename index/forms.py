from django import forms
from django.forms import ModelForm, ValidationError
from .models import User , Item , ItemStatus , Review , Transaction
import re

class User_form(ModelForm):
    password_confirm = forms.CharField(
        max_length=255,
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = User
        fields = [
            'user_id',  # Keep user_id from the model
            'username',
            'password',
            'password_confirm',
            'email',
            'first_name',
            'middle_name',
            'last_name',
            'phone_number',
            'image',
        ]
        widgets = {
            'user_id': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'user_id': 'College ID',  # Change label for user_id to "College ID"
            'image': 'image (Optional)',  # Change label for user_id to "College ID"
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("This username is already taken.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'\d', password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r'[A-Z]', password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        return password

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return password_confirm

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if len(phone) != 10:
            raise ValidationError("Phone number must be exactly 10 digits long.")
        if not phone.startswith('05'):
            raise ValidationError("Phone number must start with '05'.")
        if not phone.isdigit():
            raise ValidationError("Phone number must contain only digits.")
        return phone

    def clean_user_id(self):
        user_id = str(self.cleaned_data.get('user_id'))
        if len(user_id) != 9:
            raise ValidationError("College ID must be exactly 9 digits long.")
        if not user_id.isdigit():
            raise ValidationError("College ID must contain only numeric digits.")
        return user_id


class Item_form(ModelForm):
      
    class Meta:
        model = Item
        fields = ['title','description','price','category','condition','image']
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(Item_form, self).__init__(*args, **kwargs)

    def clean_user(self):
        user = self.cleaned_data.get('user')
        if user != self.current_user:
            raise forms.ValidationError("You can only register items with your own user ID.")
        
        return user 
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be a positive number.")
        if price > 100000:
            raise forms.ValidationError("Price cannot exceed 10,000.")
    
        return price
    def clean_rating(self):
        rating = self.cleaned_data.get('rating')
        if rating < 1 or rating > 5:
            raise forms.ValidationError("Rating must be between 1 and 5.")   
        return rating

class ItemStatus_form(ModelForm):
    class Meta:
        model = ItemStatus
        fields = '__all__'                   

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('user', None)
        super(ReviewForm, self).__init__(*args, **kwargs)

    def clean_user(self):
        user = self.cleaned_data.get('reviewer')
        if user != self.current_user:
            raise forms.ValidationError("You can only review with your own user ID.")        

class TransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = '__all__'    
