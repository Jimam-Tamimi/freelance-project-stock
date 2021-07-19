from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, Http404

from . forms import *
from . serializers import *

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
    
    # portfolio = Portfolio.objects.get(id=pk)
    serializer = PortfolioSerializer(portfolio, many=False)
    
    # for rendering Modal Portfolio Create Form from sidebar
    modalPortfolioForm = PortfolioForm()
    modalWatchlistForm = WatchlistForm()  
    
    # for rendering Modal BuySell Stock Form 
    transaction = TransactionForm() 

    # stock = Stock.objects.get(portfolio=portfolio)
    # stockSerializer = StockSerializer(stock, many=True)
    


    context = {'portfolio': serializer.data, 
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
    
    context = {'watchlist': serializer.data, 
                'form': form, 
                'modalPortfolioForm': modalPortfolioForm,
                'modalWatchlistForm': modalWatchlistForm
                }
    
    return render(request, 'dashboard/watchlist.html', context)
