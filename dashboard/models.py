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
    description = models.TextField(max_length=2000, blank=True, null=True)
    # description = RichTextField( blank=True, null=True)
    live_quotes = models.BooleanField(default=True)
    update_every = models.IntegerField(null=True, default=10)
    default_commission = models.FloatField(null=True, default=0, blank=True)
    cash = models.FloatField(default=0, null=True, blank=True)
    # include_cash_balance = models.BooleanField(default=True)
    portfolio_percentage = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    days_held = models.IntegerField(null=True, default=0)
    current_value = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    profit = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    profit_percentage = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    
    #pip install django-moneyfield
    currency = models.CharField(max_length=5, default='INR')
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    # declares a field to display on the Django admin or anytime you want string representation of the entire object; must be unique
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
    
    



class StockDetail(models.Model):
    """
    A stock detail belonging to a Portfolio.
    """
    # Stock will be deleted, if Portfolio is deleted
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stockdetails')
    
    # from Quotes API
    longName = models.CharField('Name', null=True, max_length=150)    
    # regularMarketPrice = models.DecimalField('Current Price', null=True, default=0, decimal_places=2, max_digits=15)
    regularMarketTime = models.DateField('Last Price Update Date and Time', null=True)
    regularMarketChange = models.DecimalField('Day Change', null=True, default=0, decimal_places=2, max_digits=15)
    regularMarketChangePercent = models.DecimalField('Day Change %', null=True, default=0, decimal_places=2, max_digits=15)
    regularMarketDayLow = models.DecimalField('Day Lo', null=True, default=0, decimal_places=2, max_digits=15)
    regularMarketDayHigh = models.DecimalField('Day Hi', null=True, default=0, decimal_places=2, max_digits=15)
    fiftyTwoWeekLow = models.DecimalField('52 Week Lo', null=True, default=0, decimal_places=2, max_digits=15)
    fiftyTwoWeekHigh = models.DecimalField('52 Week Hi', null=True, default=0, decimal_places=2, max_digits=15)
    regularMarketVolume = models.PositiveBigIntegerField('Volume', null=True, default=0)
    averageDailyVolume10Day = models.PositiveBigIntegerField('Volume Average 10 days', null=True, default=0)
    averageDailyVolume3Month = models.PositiveBigIntegerField('Volume Average 3M', null=True, default=0)
    marketCap = models.DecimalField('Mkt Cap', null=True, default=0, decimal_places=2, max_digits=15)
    epsTrailingTwelveMonths = models.DecimalField('EPS', null=True, default=0, decimal_places=2, max_digits=15)
    trailingPE = models.DecimalField('P/E', null=True, default=0, decimal_places=2, max_digits=15)
    priceToBook = models.DecimalField('P/B', null=True, default=0, decimal_places=2, max_digits=15)
    
    
    # from Stock API
    enterpriseToEbitda = models.DecimalField('EV/ EBITDA', null=True, default=0, decimal_places=2, max_digits=15)
    trailingAnnualDividendYield = models.DecimalField('Dividend Yield', null=True, default=0, decimal_places=2, max_digits=15)
    debtToEquity = models.DecimalField('D/E', null=True, default=0, decimal_places=2, max_digits=15)
    returnOnEquity = models.DecimalField('ROE', null=True, default=0, decimal_places=2, max_digits=15)
    returnOnAssets = models.DecimalField('ROA', null=True, default=0, decimal_places=2, max_digits=15)
    totalRevenue = models.DecimalField('Revenues', null=True, default=0, decimal_places=2, max_digits=15)
    ebitda = models.DecimalField('EBITDA', null=True, default=0, decimal_places=2, max_digits=15)
    netIncome = models.DecimalField('Net Profit', null=True, default=0, decimal_places=2, max_digits=15)
    sector = models.CharField('Sector', null=True, blank=True, max_length=250)
    industry = models.CharField('Industry', null=True, blank=True, max_length=250)
    website = models.CharField('Website', null=True, blank=True, max_length=250)
    
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
    
    # from Quotes API
    symbol = models.CharField('Symbol', max_length=20)
    regularMarketPrice = models.DecimalField('Current Price', null=True, default=0, decimal_places=2, max_digits=15)
    
    
    # from User
    quantity = models.IntegerField('Shares', null=True, default=0)
    purchase_date = models.DateField('Purchase Date', auto_now_add=True, auto_now=False, null=True)
    buyPrice = models.DecimalField('Buy Price', null=True, default=0, decimal_places=2, max_digits=15)
    adjusted_buy_price = models.DecimalField('Adjusted Buy Price', null=True, default=0, decimal_places=2, max_digits=15)
    purchase_cost = models.DecimalField('Purchase Cost', null=True, default=0, decimal_places=2, max_digits=15)
    comments = models.TextField('Comments', max_length=1000, blank=True, null=True)
    
    commissions = models.DecimalField('Commissions', null=True, default=0, decimal_places=2, max_digits=15)
    fees = models.DecimalField('Fees', null=True, default=0, decimal_places=2, max_digits=15)
    update_cash_balance = models.BooleanField('Update Cash', default=True)
    # comments = RichTextField( blank=True, null=True)
    transaction_type = models.CharField('Transaction Type', max_length=10, choices = TRANSACTION_TYPE_CHOICES)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')
    
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
    

    
    
