"""
URL configuration for e_commerce_jic project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from index import views
from django.conf import settings
from django.conf.urls.static import static


# A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U,
#  V, W, X, Y, Z.

# there are :a c d i
urlpatterns = [
    path('account',views.account,name='account' ),
    path('admin/', admin.site.urls),
    path('cart', views.cart, name='cart'),
    path('display_personal_information', views.display_personal_information, name='display_personal_information'),
    path('favourite', views.favourite, name='favourite'),
    path('index', views.index, name='index'),
    path('item_details/<int:item_id>', views.item_details, name='item_details'),
    path('item_register', views.item_register, name='item_register'),
    path('reset_password', views.reset_password, name='reset_password'),
    path('review/<int:transaction_id>', views.review, name='review'),
    path('user_login', views.user_login, name='login'),
    path('update_account', views.update_account, name='update_account'),
    path('transaction', views.transaction, name='transaction'),
    path('transaction_seller', views.transaction_seller, name='transaction_seller'),
    path('update_item/<int:item_id>', views.update_item, name='update_item'),
    path('user_register', views.user_register, name='user_register'),
    path('user_logout', views.user_logout, name='logout'),
    path('', views.welcome, name='welcome'),
    path('your_item', views.your_item, name='your_item'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
