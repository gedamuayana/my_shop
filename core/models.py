from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# 1. የተጠቃሚው የገንዘብ ኪስ (Wallet)
class UserWallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    daily_orders_done = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.balance} Birr"

@receiver(post_save, sender=User)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        UserWallet.objects.create(user=instance)

# 2. የገንዘብ ማስቀመጫ ጥያቄ (Deposit Request)
class DepositRequest(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'በጥበቃ ላይ'),
        ('Approved', 'የጸደቀ'),
        ('Rejected', 'የተሰረዘ'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    cbe_screenshot = models.ImageField(upload_to='deposit_receipts/')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} Birr ({self.status})"

# 3. የገንዘብ ማውጫ ጥያቄ (Withdraw Request) - ከDepositRequest ውጭ መሆን አለበት
class WithdrawRequest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bank_account = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"