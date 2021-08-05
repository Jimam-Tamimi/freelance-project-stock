from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField

import requests
import json

from requests.api import request
from django.utils import timezone

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
  

def get_stockDetails(symbol):
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
        
        

        response = requests.get(url, headers=headers).json()

        # print('Getting Stock Details')
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
        
        try:
            stock_details['trailingPE'] = resultsArray['trailingPE']
        except:
            stock_details['trailingPE'] = 0
            
        stock_details['priceToBook'] = resultsArray['priceToBook']


        url = "https://rest.yahoofinanceapi.com/v11/finance/quoteSummary/" + symbol
        
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

    
class Stock(models.Model):
    """
    A stock belonging to a Portfolio.
    """
    symbol = models.CharField('Symbol', max_length=20)
    quantity = models.IntegerField('Shares', null=True, default=0)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='stocks')

    
    

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
    
    def save(self, *args, **kwargs):
        # print('I am in saving Stock Detail in Stock Model')
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
    purchase_date = models.DateField('Purchase Date', auto_now_add=True, auto_now=False, null=True)
    regularMarketPrice = models.DecimalField('Buy Price', null=True, default=0, decimal_places=2, max_digits=15)
    adjusted_buy_price = models.DecimalField('Adjusted Buy Price', null=True, default=0, decimal_places=2, max_digits=15)
    purchase_cost = models.DecimalField('Purchase Cost', null=True, default=0, decimal_places=2, max_digits=15)
    comments = models.TextField('Comments', max_length=1000, blank=True, null=True)
    commissions = models.DecimalField('Commissions', null=True, default=0, decimal_places=2, max_digits=15)
    fees = models.DecimalField('Fees', null=True, default=0, decimal_places=2, max_digits=15)
    update_cash_balance = models.BooleanField('Update Cash', default=True)
    # comments = RichTextField( blank=True, null=True)
    transaction_type = models.CharField('Transaction Type', max_length=10, choices = TRANSACTION_TYPE_CHOICES)
    
    # Transactions will be deleted, if Portfolio is deleted
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='transactions')    
    
    
    
    
    # calculations
    portfolio_percentage = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    days_held = models.IntegerField(null=True, default=0)
    current_value = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    profit = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    profit_percentage = models.DecimalField(null=True, default=0, decimal_places=2, max_digits=15)
    

    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True)
    
    def __str__(self):
        return self.symbol
    
    def save(self, *args, **kwargs):
        ''' On save, update timestamps '''
        if not self.id:
            self.created = timezone.now()
        self.modified = timezone.now()
        
        # print('self.')
        # print(self.quantity)
        # print('pc.')
        # print(self.purchase_cost)
        self.current_value = self.quantity * StockDetail.objects.get(symbol=self.symbol).regularMarketPrice
        self.portfolio_percentage = 9999
        self.days_held = 10
        # print('cv.')
        # print(self.current_value)
        # print(self.purchase_cost)

        self.profit = self.current_value - Decimal(self.purchase_cost)
        self.profit_percentage = (self.current_value / Decimal(self.purchase_cost)) - 1
        
        return super().save(*args, **kwargs)
    
    def update_fields(self):
        self.save()
    
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
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name='wathcliststocks')
    
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
    
    created = models.DateTimeField(auto_now_add=True, auto_now=False, null=True)
    modified = models.DateTimeField(auto_now_add=True, null=True)
    
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
    
