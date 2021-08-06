from django.http.response import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status


from . serializers import *
from . models import *
from . permissions import IsOwnerOrReadOnly, IsPortfolioOwnerOrReadOnly
from django.db.models import Q

import requests
import json


def get_stock_details(symbol):
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

    # print(response)
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

    url = "https://rest.yahoofinanceapi.com/v11/finance/quoteSummary/" + symbol
     
    querystring = {"modules":"summaryDetail,assetProfile,financialData,defaultKeyStatistics,incomeStatementHistory"}
       
    quoteResponse = requests.get(url, headers=headers, params=querystring).json()
    
    newResultsArray = quoteResponse['quoteSummary']['result'][0]
    
    stock_details['enterpriseToEbitda'] = newResultsArray['defaultKeyStatistics']['enterpriseToEbitda']['fmt']
    stock_details['trailingAnnualDividendYield'] = newResultsArray['summaryDetail']['trailingAnnualDividendYield']['fmt']
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
    return JsonResponse(stock_details, safe=False)


def get_stockDetails(symbol):
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

    # print('Adding Stock Details')
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


    url = "https://rest.yahoofinanceapi.com/v11/finance/quoteSummary/" + symbol
     
    querystring = {"modules":"summaryDetail,assetProfile,financialData,defaultKeyStatistics,incomeStatementHistory"}
       
    quoteResponse = requests.get(url, headers=headers, params=querystring).json()
    
    newResultsArray = quoteResponse['quoteSummary']['result'][0]
    
    stock_details['enterpriseToEbitda'] = newResultsArray['defaultKeyStatistics']['enterpriseToEbitda']['fmt']
    # stock_details['trailingAnnualDividendYield'] = newResultsArray['summaryDetail']['trailingAnnualDividendYield']['fmt']
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


 
def get_stocks_suggestions(request):
    '''
    api/suggestions/
    '''
    
    # if request.is_ajax():
    param = request.GET.get("q")
            
    url = "https://rest.yahoofinanceapi.com/v6/finance/autocomplete?region=IN&lang=en&query=" + param 


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

    # print(response)
    # print(response)
    suggestions = []
    resultsArray = response['ResultSet']['Result']
    for result in resultsArray:
        # suggestions.append(result['symbol'] + " | " + result['name'] + " | " + result['exchDisp'] + " - " + result['typeDisp'])
        suggestions.append(result['symbol'])
        
    return JsonResponse(suggestions, safe=False)
    
    


def get_stocks_price(request):
    if request.is_ajax():
        # print('get_stocks_price for -')
        symbol = request.GET.get("q")
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

        # print(response['quoteResponse']['result'][0]['regularMarketPrice'])
        # print(response)
        return JsonResponse(response['quoteResponse']['result'][0]['regularMarketPrice'], safe=False)
    
    
def get_stocks_price_util(symbol):
    # print('get_stocks_price_util for' + symbol)
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

    # print(response['quoteResponse']['result'][0]['regularMarketPrice'])
    # print(response)
    return response['quoteResponse']['result'][0]['regularMarketPrice']



@api_view(['GET', 'POST'])
def portfolioList(request):
    
    """
    /api/portfolios/
        GET: Get all portfolios.    
        POST: Create portfolio    
    """
    if request.method == 'GET':
        username = request.user
        if username:
            user = User.objects.get(username=username)
            queryset = Portfolio.objects.filter(user=user)
        else:
            queryset = Portfolio.objects.all()
            
        serializer = PortfolioSerializer(queryset, many=True)

        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PortfolioSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def portfolioDetail(request, pk):
    try:
        portfolio = Portfolio.objects.get(id=pk)
    except Portfolio.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = PortfolioSerializer(portfolio, many=False)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = PortfolioSerializer(portfolio, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        portfolio = Portfolio.objects.get(id=pk)
        portfolio.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class StocksList(generics.ListAPIView):
    """
    api/portfolios/<str:portfolio_id>/stocks/
        GET: Get portfolio's stock holdings.
    """
    serializer_class = StockSerializer

    def get_queryset(self):
        portfolio = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        return Stock.objects.filter(portfolio=portfolio)


class StocksDetailList(generics.ListAPIView):
    """
    /api/stocks/
        GET: Get stock details.
    """
    serializer_class = StockDetailSerializer

    def get_queryset(self):
        # p = get_object_or_404(Stock, id=self.kwargs['portfolio_id'])
        return StockDetail.objects.all()
    

class TransactionsList(generics.ListCreateAPIView):
    """
    /api/portfolios/<portfolio_id>/transactions/
        GET: Get list of portfolio's transactions.
        POST: Create a transaction. Must be authenticated. JSON payload must contain:
            "ticker": Ticker of security you want to transact.
            "quantity": Number of units you want to transact.
            "transaction_type": Either "Buy" or "Sell"
    """
    serializer_class = TransactionSerializer
    permission_classes = (IsPortfolioOwnerOrReadOnly, )

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        # Return transactions in reverse order to get most recent
        # transactions first. [::-1]
        return Transaction.objects.filter(portfolio=p).order_by('-created')
    
    
    def perform_create(self, serializer):
        # print('in POST')
        # Assign request data to local variables
        portfolio = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        # print('Portfolio' + portfolio.name)
        symbol = self.request.data['symbol'].upper()
        
        requested_quantity = int(self.request.data['quantity'])
        if requested_quantity <= 0:
            print('Cannot transact negative units.')
            raise ValidationError("Cannot transact negative units.")
        transaction_type = self.request.data['transaction_type']
        
        # Get price of ticker and total transaction amount
        # price = get_yahoo_quote(ticker)[ticker]['price']
        # price = get_stocks_price_util(symbol)
        # print(self.request.data)
        price = float(self.request.data['regularMarketPrice'])
        # price = 23.01
        # print(price)
        
        commissions = float(self.request.data['commissions'])
        fees = float(self.request.data['fees'])
        
        transaction_amount = round(float(requested_quantity) * price, 2) + commissions + fees
        purchase_cost = transaction_amount
        adjusted_buy_price = transaction_amount
        # print(transaction_amount)
        # print('transaction_amount')
        
        
        # current_transaction = portfolio.transactions.filter(symbol=symbol, quantity__gt = 0).order_by('-created').first()
        
        # Get the held stock if it already exists in the portfolio. Otherwise held_stock is None
        held_stock = Stock.objects.filter(symbol=symbol, portfolio=portfolio).first()


        if transaction_type == 'BUY':
            # Check if portfolio has sufficient funds to execute transaction
            if transaction_amount > portfolio.cash:
                print('Insufficient cash to buy')
                raise ValidationError(
                    'Insufficient cash to buy {} shares of {}'.format(
                        requested_quantity,
                        symbol
                    )
                )
                
                 
            if held_stock:
                # print('current_transaction = ' + current_transaction.symbol)
                held_stock.quantity += requested_quantity
                if held_stock.quantity == 0:
                    held_stock.delete()
                else:
                    held_stock.save()
                    
            else:  # ticker doesn't exist in portfolio, create new Stock
                
                held_stock = Stock(
                    symbol= symbol,
                    quantity = requested_quantity,
                    portfolio = portfolio
                )
                held_stock.save()
                print('New Stock Added in Prtfolio')
                
                
                # check if ticker exists in global stock  create new Stock
                global_stock = StockDetail.objects.filter(symbol=symbol).first()
                if global_stock:
                    pass
                else:
                    new_stock = StockDetail(
                        symbol= symbol,
                    )
                    new_stock.save()
                    print('New Stock Added in Details')
            
            portfolio.cash -= transaction_amount
            portfolio.save()   
            print('Stock BOUGHT, now saving details')
                

        # FIFO to be implemented as SELL 
        elif transaction_type == 'SELL':
            # If you hold more units than you want to sell, proceed.
            # transactions = Transaction.objects.filter(symbol=symbol)
            # print('SELL')
            # print(held_stock)
            # print(held_stock.id)
            # print(held_stock.quantity)
            # print(requested_quantity)
            # print(portfolio.cash)     
               
            if held_stock and held_stock.quantity >= requested_quantity:

                held_stock.quantity -= requested_quantity
                if held_stock.quantity == 0:  
                    print('Deleting stock instance')                  
                    held_stock.delete()
                    held_stock.save()
                else:
                    held_stock.save()
                    
                portfolio.cash += transaction_amount
                portfolio.save()
            
            # print(held_stock.quantity)
            # print(requested_quantity)
            # print(portfolio.cash)           
            print('Stock SOLD, now saving details')
        
            
        # print(detail)
        serializer.save(
                        symbol=symbol, 
                        portfolio=portfolio,
                        purchase_cost=purchase_cost, 
                        adjusted_buy_price=adjusted_buy_price
                        )
    
    
def get_charts_data(request, symbolrange):
    
    # print(datetime.fromtimestamp(float(parse_qs(url)["date"][0])))
    # print('get_charts_data')
    symbol = symbolrange.split('delimeter')[0]
    chartrange = symbolrange.split('delimeter')[1]
    
    if 'DOT' in symbol:
        symbol = symbol.replace('DOT', '.')
    # print(symbol)
    # print(chartrange)
    url = "https://rest.yahoofinanceapi.com/v8/finance/chart/" + symbol
    # print(url)
    querystring = {"range":chartrange,
                   "interval":"1d"}

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
    # print(response)
    timestamps = response['chart']['result'][0]['timestamp']
    close = response['chart']['result'][0]['indicators']['quote'][0]['close']
    high = response['chart']['result'][0]['indicators']['quote'][0]['high']
    low = response['chart']['result'][0]['indicators']['quote'][0]['low']
    open = response['chart']['result'][0]['indicators']['quote'][0]['open']
    volume = response['chart']['result'][0]['indicators']['quote'][0]['volume']

    
    ohlc = []
    for key in range(len(timestamps)):

        try:
            data_open = round(open[key],2)
        except:
            data_open = open[key]
            # print(data_open)
            
        try:
            data_high = round(high[key],2)
        except:
            data_high = high[key]
            
        try:
            data_low = round(low[key],2)
        except:
            data_low = low[key]
            
        try:
            data_close = round(close[key],2)
        except:
            data_close = close[key]
            
        ohlc.append([
                    int(str(timestamps[key])+'000'), 
                     data_open, 
                     data_high, 
                     data_low, 
                     data_close, 
                     volume[key]
                     ])

    # print('Total data we have ' + str(len(timestamps)))
    # dictionary = [[34, 61, 82],[34, 61, 82],[34, 61, 82]]
    # jsonString = json.dumps(ohlc, indent=4)
    return JsonResponse(ohlc, safe=False)



@api_view(['GET', 'POST'])
def watchList(request):
    
    """
    /api/watchlist/
        GET: Get all watchList.    
        POST: Create watchlist    
    """
    if request.method == 'GET':
        username = request.user
        if username:
            user = User.objects.get(username=username)
            queryset = Watchlist.objects.filter(user=user)
        else:
            queryset = Watchlist.objects.all()
            
        serializer = WatchlistSerializer(queryset, many=True)
        
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WatchlistSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST', 'DELETE'])
def watchListDetail(request, pk):
    try:
        watchlist = Watchlist.objects.get(id=pk)
    except Watchlist.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = WatchlistSerializer(watchlist, many=False)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WatchlistSerializer(watchlist, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        watchlist = Watchlist.objects.get(id=pk)
        watchlist.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WatchlistStocksList(generics.ListCreateAPIView):
    
    """
    /api/watchlists/<watchlist_id>/stocks/
        GET: Get list of watchlists stocks.
        POST: Create a stocks. Must be authenticated. JSON payload must contain:
            "ticker": Ticker of security you want to transact.
    """
    serializer_class = WatchlistStockSerializer

    def get_queryset(self):
        w = get_object_or_404(Watchlist, id=self.kwargs['watchlist_id'])
        # Return transactions in reverse order to get most recent
        # transactions first. [::-1]
        return WatchlistStock.objects.filter(watchlist=w)
    
    
    def perform_create(self, serializer):
        # print('in POST')
        # Assign request data to local variables
        watchlist = get_object_or_404(Watchlist, id=self.kwargs['watchlist_id'])
        # print('Watchlist - ' + watchlist.watchlist_name)
        symbol = self.request.data['symbol'].upper()
        # print(symbol)
        
        
        new_stock = WatchlistStock(
            symbol=symbol,
            watchlist=watchlist
        )
        new_stock.save()
           
        # print('Stock Saved, now saving details')

        serializer.save(symbol=symbol, watchList=watchlist)
        
        
        

