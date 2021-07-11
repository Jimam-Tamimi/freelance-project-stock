from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import viewsets, permissions, generics
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework import status


from . serializers import *
from . models import *
from . permissions import IsOwnerOrReadOnly, IsPortfolioOwnerOrReadOnly


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
    /api/portfolios/<portfolio_id>/stocks/
        GET: Get portfolio's stock holdings.
    """
    serializer_class = StockSerializer

    def get_queryset(self):
        p = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        return Stock.objects.filter(portfolio=p)




@api_view(['GET'])
def stockDetail(request, pk):
    stock = Stock.objects.get(id=pk)
    serializer = StockSerializer(stock, many=False)
    
    return Response(serializer.data)


@api_view(['POST'])
def stockCreate(request):
    serializer = StockSerializer(data=request.data)
    print('API CREATE')
    print(request.data)
    if serializer.is_valid():
        print('API VALID')
        # serializer.save()
        serializer.save(portfolio=request.portfolio)
        
    return Response(serializer.data)


@api_view(['POST'])
def stockUpdate(request, pk):
    stock = Stock.objects.get(id=pk)
    serializer = StockSerializer(instance=stock, data=request.data)
    print('API UPDATE')
    print(request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


@api_view(['DELETE'])
def stockDelete(request, pk):
    stock = Stock.objects.get(id=pk)
    stock.delete()
        
    return Response('Items Successfully deleted')





@api_view(['GET'])
def transactionDetail(request, pk):
    portfolio_id = Portfolio.objects.get(id=pk)
    transaction = Transaction.objects.filter(portfolio=portfolio_id)

    serializer = TransactionSerializer(transaction, many=True)
    return Response(serializer.data)
    
    
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
        # transactions first.
        return Transaction.objects.filter(portfolio=p)[::-1]
    
    
    def perform_create(self, serializer):
        print('in POST')
        # Assign request data to local variables
        portfolio = get_object_or_404(Portfolio, id=self.kwargs['portfolio_id'])
        print('Portfolio' + portfolio.name)
        symbol = self.request.data['symbol'].upper()
        
        requested_quantity = int(self.request.data['quantity'])
        if requested_quantity <= 0:
            raise ValidationError("Cannot transact negative units.")
        transaction_type = self.request.data['transaction_type']
        
        # Get price of ticker and total transaction amount
        # price = get_yahoo_quote(ticker)[ticker]['price']
        price = 500
        
        transaction_amount = round(requested_quantity * price, 2)
        # Get the held stock if it already exists in the portfolio. Otherwise held_stock is None
        held_stock = portfolio.stocks.filter(symbol=symbol).first()

        if transaction_type == 'Buy':
            # Check if portfolio has sufficient funds to execute transaction
            if transaction_amount > portfolio.cash:
                raise ValidationError(
                    'Insufficient cash to buy {} shares of {}'.format(
                        requested_quantity,
                        symbol
                    )
                )
            portfolio.cash -= transaction_amount
            portfolio.save()
            if held_stock:
                held_stock.quantity += requested_quantity
                if held_stock.quantity == 0:
                    held_stock.delete()
                else:
                    held_stock.save()
            else:  # ticker doesn't exist in portfolio, create new Stock
                new_stock = Stock(
                    symbol=symbol,
                    quantity=requested_quantity,
                    portfolio=portfolio
                )
                new_stock.save()

        elif transaction_type == 'Sell':
            # If you hold more units than you want to sell, proceed.
            if held_stock and held_stock.quantity >= requested_quantity:
                portfolio.cash += transaction_amount
                portfolio.save()
                held_stock.quantity -= requested_quantity
                if held_stock.quantity == 0:
                    held_stock.delete()
                else:
                    held_stock.save()
            

        serializer.save(symbol=symbol, portfolio=portfolio, price=price)
    
    