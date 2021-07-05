from django.http.response import JsonResponse
from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.decorators import api_view

from . serializers import *
from . models import *

@api_view(['GET'])
def apiOverview(request):
    
    api_urls={
        'List':'/portfolio-list/',
        'Detail': '/portfolio-detail/<str-pk>/',
        'Create':'/portfolio-create/',
        'Update':'/portfolio-update/<str-pk>/',
        'Delete':'/portfolio-delete/<str-pk>/',
    }
    return Response(api_urls)


@api_view(['GET'])
def portfolioList(request):
    portfolios = Portfolio.objects.all()
    serializer = PortfolioSerializer(portfolios, many=True)
    
    return Response(serializer.data)


@api_view(['GET'])
def portfolioDetail(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    serializer = PortfolioSerializer(portfolio, many=False)
    
    return Response(serializer.data)


@api_view(['POST'])
def portfolioCreate(request):
    serializer = PortfolioSerializer(data=request.data)
    print('API CREATE')
    print(request.data)
    if serializer.is_valid():
        print('API VALID')
        serializer.save()
        
    return Response(serializer.data)


@api_view(['POST'])
def portfolioUpdate(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    serializer = PortfolioSerializer(instance=portfolio, data=request.data)
    print('API UPDATE')
    print(request.data)
    
    if serializer.is_valid():
        serializer.save()
        
    return Response(serializer.data)


@api_view(['DELETE'])
def portfolioDelete(request, pk):
    portfolio = Portfolio.objects.get(id=pk)
    portfolio.delete()
        
    return Response('Items Successfully deleted')