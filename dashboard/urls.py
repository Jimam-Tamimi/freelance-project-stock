from django.urls import path
from django.conf.urls import url, include

from . import views
from . import apis



urlpatterns = [
        
    # AJAX 
    path('api/suggestions/', apis.get_stocks_suggestions),
    path('api/price/', apis.get_stocks_price),
    path('api/stock/<str:symbol>/', apis.get_stock_details),
    
    
    # # Views Name attribute is linked in Account URL LOGIn, as lazy reverse 
    path('', views.listView, name='portfolios'),
    path('portfolios/<str:pk>/', views.portfolioView),
    
    
    #API
    path('api/portfolios/', apis.portfolioList),
    path('api/portfolios/<str:pk>/', apis.portfolioDetail),
   
    # path('api/portfolios/<str:pk>/transactions/', apis.transactionDetail),
    path('api/portfolios/<str:portfolio_id>/transactions/', apis.TransactionsList.as_view()), # Not working with datatable API
    
    path('api/portfolios/<str:portfolio_id>/stocks/', apis.StocksList.as_view()),
    path('api/stock-detail/<str:pk>/', apis.stockDetail),
    path('api/stock-create/', apis.stockCreate),
    path('api/stock-update/<str:pk>/', apis.stockUpdate),
    path('api/stock-delete/<str:pk>/', apis.stockDelete),
]
