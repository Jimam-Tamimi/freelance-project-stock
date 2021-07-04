from django.db import models


class Portfolio(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(max_length=2000, blank=True, null=True)
    live_quotes = models.BooleanField(null=True)
    update_every = models.IntegerField(null=True, default=5)
    default_commission = models.FloatField(null=True, default=0)
    include_cash_balance = models.BooleanField(null=True)
    update_cash_balance_with_transaction = models.BooleanField(null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.name
