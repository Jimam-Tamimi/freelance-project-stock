from django.shortcuts import render
from . forms import *

def list(request):
    
    modalPortfolioForm = PortfolioForm()    
    return render(request, 'dashboard/dashboard.html', {'form': modalPortfolioForm})


    
    
    
