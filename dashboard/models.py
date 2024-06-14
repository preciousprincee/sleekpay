
# from django.db import models
# from decimal import Decimal
# from django.contrib.auth.models import User

# class Transaction(models.Model):
#     sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE, default=None)
#     receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE, default=None, null=True)
#     deposit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     transfer = models.DecimalField(max_digits=10, decimal_places=2, default=0)
#     new_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
  


# class AccountBalance(models.Model):
#     transactions = models.ManyToManyField(Transaction)
#     user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_balance' , default=None)
#     balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)


from django.db import models
from django.contrib.auth.models import User

class ProfilePicture(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile_picture')
    image = models.ImageField(upload_to='profile_pictures', default='blank-profile-picture.png')


class Transaction(models.Model):
    sender = models.ForeignKey(User, related_name='sent_transactions', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_transactions', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0) 
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction from {self.sender} to {self.receiver} on {self.date}"


class AccountBalance(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='account_balance')
    balance_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"Account Balance of {self.user.username}"


        