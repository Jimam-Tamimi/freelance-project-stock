from django.urls import path
from django.conf.urls import url, include
# from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from .views import *
# from rest_framework.routers import DefaultRouter

# from . import apis

# router = DefaultRouter()

urlpatterns = [
    # # API views
    # url(r'^', include(router.urls)),
    # url(r'^registration/$', apis.RegistrationAPI.as_view(), name='register'),
    # url(r'^login/$', apis.LoginView.as_view(), name='login'),
    # url(r'^user/$', apis.UserDetailsAPI.as_view(), name='users'),
    
    
    # Ui Views
    # path('signup/', CustomLoginView.as_view(), name="login"),    
    # path('login/', CustomLoginView.as_view(), name="login"),    
    # path('logout/', LogoutView.as_view(next_page='login'), name="logout"),    
    path('signup/', AccountSignup, name="login"),    
    path('login/',AccountLogin, name="login"),    
    path('logout/', AccountLogout, name="logout"),    
    path('activate/<int:id>/<str:token>/', AccountActivate, name="logout"),
    
    
    
]
