from rest_framework import serializers
from . models import *




class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        
        
class WatchlistStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchlistStock
        fields = '__all__'

        

class TransactionSerializer(serializers.ModelSerializer):    
    
    class Meta:
        model = Transaction
        fields = '__all__'
        read_only_fields = ('portfolio',)
        # fields = ('id',
        #           'symbol', 
        #           'purchase_date', 
        #           'regularMarketPrice', 
        #           'commissions', 
        #           'fees',
        #           'update_cash_balance', 
        #           'comments', 
        #           'transaction_type',
        #           'quantity',
        #           'portfolio',
        #           'created',
        #           'modified',
        # )
        
        
        
class PortfolioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    stocks = StockSerializer(many=True, read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
        # fields = ('id',
        #           'name', 
        #           'description', 
        #           'stocks', 
        #           'transactions',
        #           'live_quotes', 
        #           'update_every', 
        #           'default_commission',
        #           'cash',
        #         #   'include_cash_balance',
        #           'created',
        #           'modified',
        # )
        
        
class WatchlistSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    wathcliststocks = WatchlistStockSerializer(many=True, read_only=True)
    
    class Meta:
        model = Watchlist
        fields = '__all__'
        
        
        
        
