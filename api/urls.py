from django.urls import path
from . import views


urlpatterns = [
    path('', views.apiOverview, name="api-overview"),
    path('portfolio-list/', views.portfolioList, name="portfolio-list"),
    path('portfolio-detail/<str:pk>/', views.portfolioDetail, name="portfolio-detail"),
    path('portfolio-create/', views.portfolioCreate, name="portfolio-create"),
    path('portfolio-update/<str:pk>/', views.portfolioUpdate, name="portfolio-update"),
    path('portfolio-delete/<str:pk>/', views.portfolioDetail, name="portfolio-delete"),
]
