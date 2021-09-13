from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, Http404

from . forms import *
from . serializers import *

import time
from django.core import serializers
import aiohttp
import asyncio

from django.http import HttpResponseRedirect




    
# Login URL is provided in SETTINGS.py
@login_required()
def listView(request):
    
    modalPortfolioForm = PortfolioForm()    
    modalWatchlistForm = WatchlistForm()  
    
    return render(request, 'dashboard/dashboard.html', 
                            {'modalPortfolioForm': modalPortfolioForm,
                             'modalWatchlistForm': modalWatchlistForm
                             })



@login_required()
def portfolioView(request, pk):
   
    # for rendering individual portfolio level detail
    portfolio = get_object_or_404(Portfolio, id=pk)
    
    stocks_list = portfolio.stocks.filter()
    
    transaction_list = portfolio.transactions.filter().order_by('-created')
    
    transaction_js = serializers.serialize("json", portfolio.transactions.filter().order_by('-created'))
    stock_js = serializers.serialize("json", portfolio.stocks.all())
    
    for stock in stocks_list:
        stock.update_fields()

    # for t in transaction_list:
    #     t.update_fields()
    
        
    # portfolio = Portfolio.objects.get(id=pk)
    serializer = PortfolioSerializer(portfolio, many=False)
    
    # for rendering Modal Portfolio Create Form from sidebar
    modalPortfolioForm = PortfolioForm()
    modalWatchlistForm = WatchlistForm()  
    
    # for rendering Modal BuySell Stock Form 
    transaction = TransactionForm() 

    stockdetail = StockDetail.objects.all()
    
    # for sd in stockdetail:
    #     sd.update_fields()

    # https://julien.danjou.info/python-and-fast-http-clients/
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    coroutines = [sd.update_fields() for sd in stockdetail]
    results = loop.run_until_complete(asyncio.gather(*coroutines))  

    
    
    stockSerializer = StockDetailSerializer(stockdetail, many=True)
    
    context = {
                'portfolio': serializer.data, 
                'transactions': transaction_list,
                'transaction_js': transaction_js,
                'stock_js': stock_js,
                'stock': stockSerializer.data,
                'form': transaction, 
                'modalPortfolioForm': modalPortfolioForm,
                'modalWatchlistForm': modalWatchlistForm
            }
    
    return render(request, 'dashboard/portfolio.html', context)




@login_required()
def watchlistView(request, pk):
    # for rendering individual watchlist level detail
    watchlist = get_object_or_404(Watchlist, id=pk)
    
    serializer = WatchlistSerializer(watchlist, many=False)
    
    # for rendering Modal Portfolio Create Form from sidebar
    modalPortfolioForm = PortfolioForm()
    modalWatchlistForm = WatchlistForm()  
    
    # for rendering Modal Add Stock Form 
    form = AddToWatchlistForm() 
    
    stockdetail = StockDetail.objects.all()
    stockSerializer = StockDetailSerializer(stockdetail, many=True)

    
    context = {'watchlist': serializer.data, 
                'form': form, 
                'stock': stockSerializer.data,
                'modalPortfolioForm': modalPortfolioForm,
                'modalWatchlistForm': modalWatchlistForm
                }
    
    return render(request, 'dashboard/watchlist.html', context)


@login_required()
def portfolioView_MODIFIED(request, pk):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = TransactionForm(request.POST)
        
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/portfolios/' + request.POST['id'])
    
    # if a GET (or any other method) we'll create a blank form
    else:
        # for rendering individual portfolio level detail
        portfolio = get_object_or_404(Portfolio, id=pk)
        
        stocks_list = portfolio.stocks.filter()
        
        transaction_list = portfolio.transactions.filter().order_by('-created')
        
        transaction_js = serializers.serialize("json", portfolio.transactions.filter().order_by('-created'))
        stock_js = serializers.serialize("json", portfolio.stocks.all())
        
        for stock in stocks_list:
            stock.update_fields()

        # for t in transaction_list:
        #     t.update_fields()
        
            
        # portfolio = Portfolio.objects.get(id=pk)
        serializer = PortfolioSerializer(portfolio, many=False)
        
        # for rendering Modal Portfolio Create Form from sidebar
        modalPortfolioForm = PortfolioForm()
        modalWatchlistForm = WatchlistForm()  
        
        # for rendering Modal BuySell Stock Form 
        transaction = TransactionForm() 

        stockdetail = StockDetail.objects.all()
        
        # for sd in stockdetail:
        #     sd.update_fields()

        # https://julien.danjou.info/python-and-fast-http-clients/
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        coroutines = [sd.update_fields() for sd in stockdetail]
        results = loop.run_until_complete(asyncio.gather(*coroutines))  

        
        
        stockSerializer = StockDetailSerializer(stockdetail, many=True)
        
        context = {
                    'portfolio': serializer.data, 
                    'transactions': transaction_list,
                    'transaction_js': transaction_js,
                    'stock_js': stock_js,
                    'stock': stockSerializer.data,
                    'form': transaction, 
                    'modalPortfolioForm': modalPortfolioForm,
                    'modalWatchlistForm': modalWatchlistForm
                }
        
        return render(request, 'dashboard/portfolio.html', context)
