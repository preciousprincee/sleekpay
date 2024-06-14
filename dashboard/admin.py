from django.contrib import admin
from .models import AccountBalance, Transaction

# Register the AccountBalance model with the admin interface
admin.site.register(AccountBalance)
admin.site.register(Transaction)

# Register your models here.
