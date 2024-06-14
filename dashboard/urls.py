from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.user_register, name='register'),
    path('transfer/', views.transfer, name='transfer'),
    path('deposit/', views.deposit, name='deposit'),
    path('history/', views.history, name='history'),
    path('recipient/<str:username>/', views.recipient, name='recipient'),
    path('profile/', views.profile, name='profile'),
    path('fetch_users/', views.fetch_users, name='fetch_users'),
    path('transaction/success/', views.transaction_success, name='transaction_success'),
    path('settings/', views.settings, name='settings'),
    path('update_username/', views.update_username, name='update_username'),
    path('change_password/', views.change_password, name='change_password'),
    path('initiate-deposit/', views.initiate_deposit, name='initiate_deposit'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
]
