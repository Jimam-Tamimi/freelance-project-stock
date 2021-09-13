from rest_framework import serializers
from . models import *

class StockDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockDetail
        fields = '__all__'


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = '__all__'
        
        
        
class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
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
        
        
        
class PortfolioSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    transactions = TransactionSerializer(many=True, read_only=True)
    positions = PositionSerializer(many=True, read_only=True)
    stocks = StockSerializer(many=True, read_only=True)
    
    class Meta:
        model = Portfolio
        fields = '__all__'
            

        
        
class WatchlistSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    wathcliststocks = WatchlistStockSerializer(many=True, read_only=True)
    
    class Meta:
        model = Watchlist
        fields = '__all__'
        
class TableStateSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    
    class Meta:
        model = TableState
        fields = '__all__'  
        
        
