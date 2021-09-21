from django.urls import path
from django.conf.urls import url, include

from . import views
from . import apis



urlpatterns = [

        
    # AJAX 
    path('api/suggestions/', apis.get_stocks_suggestions),
    path('api/price/', apis.get_stocks_price),
    path('api/stock/<str:symbol>/', apis.get_stock_details),
    path('api/charts/<str:symbolrange>/', apis.get_charts_data),
    
 
    
    path('', views.listView, name='portfolios'),
    path('portfolios/<str:pk>/', views.portfolioView),
    path('watchlists/<str:pk>/', views.watchlistView),
    
    #API
    path('api/portfolios/', apis.portfolioList),
    path('api/portfolios/<str:pk>/', apis.portfolioDetail),
    path('api/watchlists/', apis.watchList),
    path('api/watchlists/<str:pk>/', apis.watchListDetail),
   
    # path('api/portfolios/<str:pk>/transactions/', apis.transactionDetail),
    path('api/portfolios/<str:portfolio_id>/transactions/', apis.TransactionsList.as_view()), # Not working with datatable API
    
    path('api/portfolios/<str:portfolio_id>/stocks/', apis.StocksList.as_view()),
    path('api/stocks/', apis.StocksDetailList.as_view()),
    path('api/watchlists/<str:watchlist_id>/stocks/', apis.WatchlistStocksList.as_view()),
    
    
    path('api/columns/', apis.listColumn), # on this url | haveyou got it?

    path('api/state/', apis.stateList),
    path('api/state/<str:table_name>/', apis.stateListDetail),
    
    # path('api/stock-detail/<str:pk>/', apis.stockDetail),
    # path('api/stock-create/', apis.stockCreate),
    # path('api/stock-update/<str:pk>/', apis.stockUpdate),
    # path('api/stock-delete/<str:pk>/', apis.stockDelete),
    
]
