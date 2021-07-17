from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


from django.http import HttpResponse, Http404

from . forms import *
from . serializers import *

# Login URL is provided in SETTINGS.py
@login_required()
def listView(request):
    
    modalPortfolioForm = PortfolioForm()    
    
    return render(request, 'dashboard/dashboard.html', 
                            {'modalPortfolioForm': modalPortfolioForm})



@login_required()
def portfolioView(request, pk):
    # for rendering individual portfolio level detail
    portfolio = get_object_or_404(Portfolio, id=pk)
    
    # portfolio = Portfolio.objects.get(id=pk)
    serializer = PortfolioSerializer(portfolio, many=False)
    
    # for rendering Modal Portfolio Create Form from sidebar
    modalPortfolioForm = PortfolioForm()
    
    # for rendering Modal BuySell Stock Form 
    transaction = TransactionForm() 

    # stock = Stock.objects.get(portfolio=portfolio)
    # stockSerializer = StockSerializer(stock, many=True)
    


    context = {'portfolio': serializer.data, 
                'form': transaction, 
                'modalPortfolioForm': modalPortfolioForm}
    
    return render(request, 'dashboard/portfolio.html', context)

    

