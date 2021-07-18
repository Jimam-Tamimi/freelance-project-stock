from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

import requests
import json

from requests.api import request

def get_stockDetails(symbol):
        url = "https://yahoo-finance-low-latency.p.rapidapi.com/v6/finance/quote?symbols=" + symbol


        headers = {
            'x-rapidapi-key': "15c09e0d16msh24199eee9546841p1521e6jsn94f58b809f42",
            'x-rapidapi-host': "yahoo-finance-low-latency.p.rapidapi.com",
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

            }
        
        

        response = requests.get(url, headers=headers).json()

        print('Adding Stock Details')
        # print(response)
        stock_details = {}
        resultsArray = response['quoteResponse']['result'][0]
        
        stock_details['symbol'] = resultsArray['symbol']
        stock_details['longName'] = resultsArray['longName']
        stock_details['regularMarketPrice'] = resultsArray['regularMarketPrice']
        stock_details['regularMarketTime'] = resultsArray['regularMarketTime']
        stock_details['regularMarketChange'] = resultsArray['regularMarketChange']
        stock_details['regularMarketChangePercent'] = resultsArray['regularMarketChangePercent']
        stock_details['regularMarketDayLow'] = resultsArray['regularMarketDayLow']
        stock_details['regularMarketDayHigh'] = resultsArray['regularMarketDayHigh']
        stock_details['fiftyTwoWeekLow'] = resultsArray['fiftyTwoWeekLow']
        stock_details['fiftyTwoWeekHigh'] = resultsArray['fiftyTwoWeekHigh']
        stock_details['regularMarketVolume'] = resultsArray['regularMarketVolume']
        stock_details['averageDailyVolume10Day'] = resultsArray['averageDailyVolume10Day']
        stock_details['averageDailyVolume3Month'] = resultsArray['averageDailyVolume3Month']
        stock_details['marketCap'] = resultsArray['marketCap']
        stock_details['epsTrailingTwelveMonths'] = resultsArray['epsTrailingTwelveMonths']
        stock_details['trailingPE'] = resultsArray['trailingPE']
        stock_details['priceToBook'] = resultsArray['priceToBook']


        url = "https://yahoo-finance-low-latency.p.rapidapi.com/v11/finance/quoteSummary/" + symbol
        
        querystring = {"modules":"summaryDetail,assetProfile,financialData,defaultKeyStatistics,incomeStatementHistory"}
        
        quoteResponse = requests.get(url, headers=headers, params=querystring).json()
        
        newResultsArray = quoteResponse['quoteSummary']['result'][0]
        
        stock_details['enterpriseToEbitda'] = newResultsArray['defaultKeyStatistics']['enterpriseToEbitda']['fmt']
        try:
            stock_details['trailingAnnualDividendYield'] = newResultsArray['summaryDetail']['trailingAnnualDividendYield']['fmt']
        except:
            stock_details['trailingAnnualDividendYield'] = 0
            
        stock_details['debtToEquity'] = newResultsArray['financialData']['debtToEquity']['raw']
        stock_details['returnOnEquity'] = newResultsArray['financialData']['returnOnEquity']['fmt']
        stock_details['returnOnAssets'] = newResultsArray['financialData']['returnOnAssets']['fmt']
        stock_details['totalRevenue'] = newResultsArray['financialData']['totalRevenue']['raw']
        stock_details['ebitda'] = newResultsArray['financialData']['ebitda']['raw']
        # stock_details['netIncome'] = newResultsArray['incomeStatementHistory']['incomeStatementHistory']['0']['netIncome']['raw']
        stock_details['sector'] = newResultsArray['assetProfile']['sector']
        stock_details['industry'] = newResultsArray['assetProfile']['industry']
        stock_details['website'] = newResultsArray['assetProfile']['website']


        print(stock_details)
        return stock_details
    
    
    
class Portfolio(models.Model):
    

    """
    A portfolio belonging to a User. A portfolio has a cash balance (defaulting to INR1000),
    stocks and transactions.
    """
    # Potfolio will be deleted, if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    name = models.CharField(max_length=128, null=True, blank=True)
    description = models.TextField(max_length=2000, blank=True, null=True)
    # sync_with_cloud = models.BooleanField(default=True)    
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
    quantity = models.PositiveBigIntegerField(null=True, default=0)
    
    # from Quotes API
    symbol = models.CharField('Symbol', max_length=20)
    longName = models.CharField('Name', null=True, max_length=150)    
    regularMarketPrice = models.DecimalField('Current Price', null=True, default=0, decimal_places=2, max_digits=15)
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
    # netIncome = models.PositiveBigIntegerField('Net Profit', null=True, default=0)
    sector = models.CharField('Sector', null=True, blank=True, max_length=250)
    industry = models.CharField('Industry', null=True, blank=True, max_length=250)
    website = models.CharField('Website', null=True, blank=True, max_length=250)
    
    created = models.DateField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
        
    def save(self, *args, **kwargs):
        
        details = get_stockDetails(self.symbol)

        self.longName = details['longName']
        self.regularMarketPrice = details['regularMarketPrice']
        # self.regularMarketTime = details['regularMarketTime']
        self.regularMarketChange = details['regularMarketChange']
        self.regularMarketChangePercent = details['regularMarketChangePercent']
        self.regularMarketDayLow = details['regularMarketDayLow']
        self.regularMarketDayHigh = details['regularMarketDayHigh']
        self.fiftyTwoWeekLow = details['fiftyTwoWeekLow']
        self.fiftyTwoWeekHigh = details['fiftyTwoWeekHigh']
        self.regularMarketVolume = details['regularMarketVolume']
        self.averageDailyVolume10Day = details['averageDailyVolume10Day']
        self.averageDailyVolume3Month = details['averageDailyVolume3Month']
        self.marketCap = details['marketCap']
        self.epsTrailingTwelveMonths = details['epsTrailingTwelveMonths']
        self.trailingPE = details['trailingPE']
        self.priceToBook = details['priceToBook']


        self.enterpriseToEbitda = details['enterpriseToEbitda']
        self.trailingAnnualDividendYield = str(details['trailingAnnualDividendYield']).replace('%', '')
        self.debtToEquity = details['debtToEquity']
        self.returnOnEquity = str(details['returnOnEquity']).replace('%', '')
        self.returnOnAssets = str(details['returnOnAssets']).replace('%', '')
        self.totalRevenue = details['totalRevenue']
        self.ebitda = details['ebitda']
        # self.netIncome = details['netIncome']
        self.sector = details['sector']
        self.industry = details['industry']
        self.website = details['website']

       
        
        super().save(*args, **kwargs)
    
    
class Transaction(models.Model):
    """
    A transaction belonging to a Portfolio.
    """
    TRANSACTION_TYPE_CHOICES = (
        ("BUY", "BUY"),
        ("SELL", "SELL"),
    )
    

    # from User
    symbol = models.CharField('Symbol', max_length=20)
    quantity = models.IntegerField('Shares', null=True, default=0)
    purchase_date = models.DateField('Purchase Date', auto_now_add=True, auto_now=False, null=True)
    price = models.DecimalField('Buy Price', null=True, default=0, decimal_places=2, max_digits=15)
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
    

    
    
    
    
    
    
    
        
        


