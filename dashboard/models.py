from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

import requests
import datetime

import json

from requests.api import request
from django.utils import timezone
from django.db.models import Count

import asyncio
import aiohttp


from decimal import *

def get_all_stockDetails_max10(symbols):
        # print(symbols)
        url = 'https://rest.yahoofinanceapi.com/v6/finance/quote'
        
        symbols = 'AAPL,IBM,MSFT,GOOG,TCS,WIPRO,IDEA,NMDC'
        
        querystring = {'symbols':symbols}


        headers = {
            'x-api-key': "AD1ayImlEG78RQNYTzFYG3rzNSEVJHXY1v5ZipcL",
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

            }
        
        

        response = requests.get(url, headers=headers, params=querystring).json()

        # print('Getting All Stock Details - Max 10')
        # print(response)
        stock_details = []
        
        for i in range(len(symbols)):                    
            resultsArray = response['quoteResponse']['result'][i]
            
            individual_stock_details = {}
            individual_stock_details['symbol'] = resultsArray['symbol']
            individual_stock_details['longName'] = resultsArray['longName']
            individual_stock_details['regularMarketPrice'] = resultsArray['regularMarketPrice']
            individual_stock_details['regularMarketTime'] = resultsArray['regularMarketTime']
            individual_stock_details['regularMarketChange'] = resultsArray['regularMarketChange']
            individual_stock_details['regularMarketChangePercent'] = resultsArray['regularMarketChangePercent']
            individual_stock_details['regularMarketDayLow'] = resultsArray['regularMarketDayLow']
            individual_stock_details['regularMarketDayHigh'] = resultsArray['regularMarketDayHigh']
            individual_stock_details['fiftyTwoWeekLow'] = resultsArray['fiftyTwoWeekLow']
            individual_stock_details['fiftyTwoWeekHigh'] = resultsArray['fiftyTwoWeekHigh']
            individual_stock_details['regularMarketVolume'] = resultsArray['regularMarketVolume']
            individual_stock_details['averageDailyVolume10Day'] = resultsArray['averageDailyVolume10Day']
            individual_stock_details['averageDailyVolume3Month'] = resultsArray['averageDailyVolume3Month']
            individual_stock_details['marketCap'] = resultsArray['marketCap']
            individual_stock_details['epsTrailingTwelveMonths'] = resultsArray['epsTrailingTwelveMonths']
            
            try:
                individual_stock_details['trailingPE'] = resultsArray['trailingPE']
            except:
                individual_stock_details['trailingPE'] = 0
                
            individual_stock_details['priceToBook'] = resultsArray['priceToBook']


            url = "https://rest.yahoofinanceapi.com/v11/finance/quoteSummary/" + symbols[i]
            
            querystring = {"modules":"summaryDetail,assetProfile,financialData,defaultKeyStatistics,incomeStatementHistory"}            
            quoteResponse = requests.get(url, headers=headers, params=querystring).json()            
            newResultsArray = quoteResponse['quoteSummary']['result'][0]
            
            individual_stock_details['enterpriseToEbitda'] = newResultsArray['defaultKeyStatistics']['enterpriseToEbitda']['fmt']
            try:
                individual_stock_details['trailingAnnualDividendYield'] = newResultsArray['summaryDetail']['trailingAnnualDividendYield']['fmt']
            except:
                individual_stock_details['trailingAnnualDividendYield'] = 0
                
            individual_stock_details['debtToEquity'] = newResultsArray['financialData']['debtToEquity']['raw']
            individual_stock_details['returnOnEquity'] = newResultsArray['financialData']['returnOnEquity']['fmt']
            individual_stock_details['returnOnAssets'] = newResultsArray['financialData']['returnOnAssets']['fmt']
            individual_stock_details['totalRevenue'] = newResultsArray['financialData']['totalRevenue']['raw']
            individual_stock_details['ebitda'] = newResultsArray['financialData']['ebitda']['raw']
            # stock_details['netIncome'] = newResultsArray['incomeStatementHistory']['incomeStatementHistory']['0']['netIncome']['raw']
            individual_stock_details['sector'] = newResultsArray['assetProfile']['sector']
            individual_stock_details['industry'] = newResultsArray['assetProfile']['industry']
            individual_stock_details['website'] = newResultsArray['assetProfile']['website']


            stock_details.append(individual_stock_details)
            # print(stock_details)
        return stock_details
  

async def get_stockDetails(symbol):
        # print(symbol)
        url = "https://rest.yahoofinanceapi.com/v6/finance/quote?symbols=" + symbol
        
        headers = {
            'x-api-key': "AD1ayImlEG78RQNYTzFYG3rzNSEVJHXY1v5ZipcL",
            'accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'en-GB,en;q=0.9,en-US;q=0.8,ml;q=0.7',
            'cache-control':'max-age=0',
            'upgrade-insecure-requests':'1',
            'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36'

            }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers) as response:
                response = response.json()
        


        
        
        

        # response = requests.get(url, headers=headers).json()

        # print('Getting Stock Details')
        # print(response)
        stock_details = {}
        resultsArray = response['quoteResponse']['result'][0]
        
        try:
            stock_details['symbol'] = resultsArray['symbol']
        except:
            stock_details['symbol'] = ''
            
        try:
            stock_details['longName'] = resultsArray['longName']
        except:
            stock_details['longName'] = ''
            
        try:
            stock_details['regularMarketPrice'] = resultsArray['regularMarketPrice']
        except:
            stock_details['regularMarketPrice'] = 0
            
        try:
            stock_details['regularMarketTime'] = resultsArray['regularMarketTime']
        except:
            stock_details['regularMarketTime'] = 0
            
        try:
            stock_details['regularMarketChange'] = resultsArray['regularMarketChange']
        except:
            stock_details['regularMarketChange'] = 0
            
        try:
            stock_details['regularMarketChangePercent'] = resultsArray['regularMarketChangePercent']
        except:
            stock_details['regularMarketChangePercent'] = 0
            
        try:
            stock_details['regularMarketDayLow'] = resultsArray['regularMarketDayLow']
        except:
            stock_details['regularMarketTime'] = 0
            
        try:
            stock_details['regularMarketDayHigh'] = resultsArray['regularMarketDayHigh']
        except:
            stock_details['regularMarketDayHigh'] = 0
            
        try:
            stock_details['fiftyTwoWeekLow'] = resultsArray['fiftyTwoWeekLow']
        except:
            stock_details['fiftyTwoWeekLow'] = 0
        
        try:
            stock_details['fiftyTwoWeekHigh'] = resultsArray['fiftyTwoWeekHigh']
        except:
            stock_details['fiftyTwoWeekHigh'] = 0
            
        try:
            stock_details['regularMarketVolume'] = resultsArray['regularMarketVolume']
        except:
            stock_details['regularMarketVolume'] = 0
            
        try:
            stock_details['averageDailyVolume10Day'] = resultsArray['averageDailyVolume10Day']
        except:
            stock_details['averageDailyVolume10Day'] = 0
            
        try:
            stock_details['averageDailyVolume3Month'] = resultsArray['averageDailyVolume3Month']
        except:
            stock_details['averageDailyVolume3Month'] = 0
            
        try:
            stock_details['marketCap'] = resultsArray['marketCap']
        except:
            stock_details['marketCap'] = 0
            
        try:
            stock_details['epsTrailingTwelveMonths'] = resultsArray['epsTrailingTwelveMonths']
        except:
            stock_details['epsTrailingTwelveMonths'] = 0
        
        try:
            stock_details['trailingPE'] = resultsArray['trailingPE']
        except:
            stock_details['trailingPE'] = 0
            
        try:
            stock_details['priceToBook'] = resultsArray['priceToBook']
        except:
            stock_details['priceToBook'] = 0
            

        url = "https://rest.yahoofinanceapi.com/v11/finance/quoteSummary/" + symbol
        querystring = {"modules":"summaryDetail,assetProfile,financialData,defaultKeyStatistics,incomeStatementHistory"}
        # quoteResponse = requests.get(url, headers=headers, params=querystring).json()
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=querystring) as response:
                quoteResponse = response.json()
        
        newResultsArray = quoteResponse['quoteSummary']['result'][0]
        
        try:
            stock_details['enterpriseToEbitda'] = newResultsArray['defaultKeyStatistics']['enterpriseToEbitda']['fmt']
        except:
            stock_details['enterpriseToEbitda'] = 0
            
        try:
            stock_details['trailingAnnualDividendYield'] = newResultsArray['summaryDetail']['trailingAnnualDividendYield']['fmt']
        except:
            stock_details['trailingAnnualDividendYield'] = 0
        
        try:   
            stock_details['debtToEquity'] = newResultsArray['financialData']['debtToEquity']['raw']
        except:
            stock_details['debtToEquity'] = 0
            
        try:   
            stock_details['returnOnEquity'] = newResultsArray['financialData']['returnOnEquity']['fmt']
        except:
            stock_details['returnOnEquity'] = 0
            
        try:   
            stock_details['returnOnAssets'] = newResultsArray['financialData']['returnOnAssets']['fmt']
        except:
            stock_details['returnOnAssets'] = 0
            
        try:   
            stock_details['totalRevenue'] = newResultsArray['financialData']['totalRevenue']['raw']
        except:
            stock_details['totalRevenue'] = 0
            
        try:   
            stock_details['ebitda'] = newResultsArray['financialData']['ebitda']['raw']
        except:
            stock_details['ebitda'] = 0
            
        try:   
            stock_details['netIncome'] = newResultsArray['incomeStatementHistory']['incomeStatementHistory']['0']['netIncome']['raw']
        except:
            stock_details['netIncome'] = 0
         
        try:   
            stock_details['sector'] = newResultsArray['assetProfile']['sector']
        except:
            stock_details['sector'] = ''
        
        try:   
            stock_details['industry'] = newResultsArray['assetProfile']['industry']
        except:
            stock_details['industry'] = ''
            
        try:   
            stock_details['website'] = newResultsArray['assetProfile']['website']
        except:
            stock_details['website'] = ''
            



        # print(stock_details)
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
    live_quotes = models.BooleanField(default=True)
    update_cash_balaces = models.BooleanField(default=True)
    update_every = models.IntegerField(null=True, default=10)
    default_commission = models.FloatField(null=True, default=0, blank=True)
    cash = models.FloatField(default=0, null=True, blank=True)
    currency = models.CharField(max_length=5, default='INR')
    
    #calculation
    total_portfolio_value = models.FloatField(default=0, null=True, blank=True)
    
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True)
    
    # declares a field to display on the Django admin or anytime 
    # you want string representation of the entire object; must be unique
    def __str__(self):
        return self.name
    

    class Meta:
        '''The ForeignKey i.e. user and portfolio name must be unique'''
        unique_together = ('user', 'name')
        # ordering = ['-name']


class Position(models.Model):
    """
    A position is a record of a Portfolio's stock holding on a given date.
    """
    datetime = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=20)
    quantity = models.IntegerField()
    price = models.FloatField()
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='positions')

    
    
class StockDetail(models.Model):
    """
    A StockDetail table for all users.
    """
    
    symbol = models.CharField('Symbol', unique=True, max_length=20)
    
    # from Quotes API
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
    
    # created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    # modified = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
    class Meta:
        ordering = ['-symbol']
    
    async def save(self, *args, **kwargs):
        print('I am in saving Stock Detail in Stock Model' + self.symbol)
        details = await get_stockDetails(self.symbol)

        self.longName = details['longName']
        self.regularMarketPrice = details['regularMarketPrice']
        self.regularMarketTime = details['regularMarketTime']
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
        self.netIncome = details['netIncome']
        self.sector = details['sector']
        self.industry = details['industry']
        self.website = details['website']


        super().save(*args, **kwargs)



    async def update_fields(self):

        self.save()
        
 
    

class Stock(models.Model):
    """
    A stock belonging to a Portfolio.
    """
    symbol = models.CharField('Symbol', max_length=20)
    quantity = models.IntegerField('Shares', null=True, default=0)
    regularMarketPrice = models.DecimalField('Current Price', null=True, default=0, decimal_places=2, max_digits=15)

    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')

    # declares a field to display on the Django admin or anytime 
    # you want string representation of the entire object; must be unique
    def __str__(self):
        return self.symbol
    
    class Meta:
        '''The ForeignKey i.e. portfolio and symbol name must be unique'''
        unique_together = ('symbol', 'portfolio')
        ordering = ['-symbol']
        
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()

        

        self.regularMarketPrice = StockDetail.objects.get(symbol=self.symbol).regularMarketPrice
        
        return super().save(*args, **kwargs)
    
    def update_fields(self):
        self.save()        
    
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
    date = models.DateField('Date', auto_now_add=True, auto_now=False, null=True)
    regularMarketPrice = models.DecimalField('Price', null=True, default=0, decimal_places=2, max_digits=15)
    cost = models.DecimalField('Net Total', null=True, default=0, decimal_places=2, max_digits=15)
    comments = models.TextField('Comments', max_length=1000, blank=True, null=True)
    commissions = models.DecimalField('Commissions', null=True, default=0, decimal_places=2, max_digits=15)
    fees = models.DecimalField('Fees', null=True, default=0, decimal_places=2, max_digits=15)
    update_cash_balance = models.BooleanField('Update the Cash balance', default=True)
    # comments = RichTextField( blank=True, null=True)
    transaction_type = models.CharField('Transaction Type', max_length=10, choices = TRANSACTION_TYPE_CHOICES)
    
    # Transactions will be deleted, if Portfolio is deleted
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')    
    
    days_held = models.IntegerField(null=True, default=0)
    current_value = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    profit = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    profit_percentage = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    portfolio_percentage = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        
        # days_held = Current Date - Purchase date
        # print(datetime.datetime.now().date())
        # print(self.date)
        try:
            delta =  datetime.datetime.now().date() - self.date
            # print(delta.days)
            self.days_held = delta.days
        except:
            self.days_held = 0
        
        self.cost = (self.quantity * self.regularMarketPrice) + self.commissions + self.fees
        

        # current_value = Current Price X Number of Shares        
        self.current_value = Decimal(self.quantity * StockDetail.objects.get(symbol=self.symbol).regularMarketPrice)
        
        # profit = Current Value - Purchase Cost
        self.profit = Decimal(self.current_value) - Decimal(self.cost)
        self.profit_percentage = (Decimal(self.current_value) / Decimal(self.cost)) - 1
        # Total Portfolio Value % =  Total CV of all stocks + Cash
        # portfolio_percentage = Current Value / Total Portfolio Value %
        cash = Decimal(Portfolio.objects.get(name=self.portfolio).cash)
        total = Decimal(self.current_value)
        total_cv_stocks = (total + cash)/100
        self.portfolio_percentage = self.current_value/total_cv_stocks
        
        return super().save(*args, **kwargs)
    

    
class Watchlist(models.Model):
    

    """
    A Watchlist belonging to a User. A Watchlist has stocks.
    """
    # Potfolio will be deleted, if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    watchlist_name = models.CharField(max_length=128, null=True, blank=True)
    watchlist_description = models.TextField(max_length=2000, blank=True, null=True)    
    watchlist_live_quotes = models.BooleanField(default=True)
    watchlist_update_every = models.IntegerField(null=True, default=10)
        
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True)
    
    # declares a field to display on the Django admin or 
    # anytime you want string representation of the entire object; must be unique
    def __str__(self):
        return self.watchlist_name
    

    class Meta:
        '''The ForeignKey i.e. user and portfolio name must be unique'''
        unique_together = ('user', 'watchlist_name')
        # ordering = ['-name']
    
    

        
class WatchlistStock(models.Model):
    """
    A wathcliststock belonging to a wathclist.
    """
    # Stock will be deleted, if Watchlist is deleted
    symbol = models.CharField('Symbol', max_length=20)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='wathcliststocks')
    start_price = models.DecimalField('Start Price', null=True, default=0, decimal_places=2, max_digits=15)
    start_date = models.DateField('Start Date', auto_now_add=True, auto_now=False, null=True)
    description = models.TextField('Description', max_length=1000, blank=True, null=True)
    
    
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
    class Meta:
        '''The ForeignKey i.e. watchlist and symbol name must be unique'''
        unique_together = ('symbol', 'watchlist')
        ordering = ['-symbol']
    
        
    
class TableState(models.Model):
    """
    A state save belonging to a User.
    """
    # TableStateSave will be deleted, if user is deleted
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tablename = models.CharField('TableName', max_length=50, blank=True, null=True)
    statedata = models.CharField('Data', max_length=5000, blank=True, null=True)

    
    def __str__(self):
        return self.tablename
    

    class Meta:
        '''The ForeignKey i.e. user and tablename name must be unique'''
        unique_together = ('user', 'tablename')
        

