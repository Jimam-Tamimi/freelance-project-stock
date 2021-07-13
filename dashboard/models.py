from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

class Portfolio(models.Model):
    """
    A portfolio belonging to a User. A portfolio has a cash balance (defaulting to INR1000),
    stocks and transactions.
    """
    # Potfolio will be deleted, if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=128, null=True, blank=True)
    # description = models.TextField(max_length=2000, blank=True, null=True)
    description = RichTextField( blank=True, null=True)
    live_quotes = models.BooleanField(default=True)
    update_every = models.IntegerField(null=True, default=5)
    default_commission = models.FloatField(null=True, default=0, blank=True)
    cash = models.FloatField(default=1000, null=True, blank=True)
    include_cash_balance = models.BooleanField(default=True)
    update_cash_balance_with_transaction = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
    

    class Meta:
        '''The ForeignKey i.e. user and portfolio name must be unique'''
        unique_together = ('user', 'name')
        # ordering = ['-name']


class Stock(models.Model):
    """
    A stock belonging to a Portfolio.
    """
    # Stock will be deleted, if Portfolio is deleted
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')
    symbol = models.CharField(max_length=20)
    quantity = models.PositiveBigIntegerField(null=True, default=0)
    
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
    
    
class Transaction(models.Model):
    """
    A transaction belonging to a Portfolio.
    """
    TRANSACTION_TYPE_CHOICES = (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
    )
    
    symbol = models.CharField(max_length=20)
    purchase_date = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    price = models.FloatField(null=True, default=5)
    commissions = models.FloatField(null=True, default=0)
    fees = models.FloatField(null=True, default=0)
    update_cash_balance = models.BooleanField(default=True)
    # comments = models.TextField(max_length=1000, blank=True, null=True) 
    comments = RichTextField( blank=True, null=True)
    transaction_type = models.CharField(max_length=10, choices = TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField(null=True, default=0)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol


    
    
    
    
