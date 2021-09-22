from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import *
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib.auth  import authenticate,  login, logout


# class CustomLoginView(LoginView):
#     template_name = 'account/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True
    
#     def get_success_url(self):
#         return reverse_lazy('portfolios')
def AccountLogin(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method ==  'GET'):
        return render(request, 'account/login.html')
    elif(request.method ==  'POST'):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.success(request, "Log In Failed")
            return redirect("/login/")

    
def AccountSignup(request):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'POST'):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        re_password = request.POST['re_password']
        if(password == re_password):
            if(len(MyUser.objects.filter(email=email)) != 0):
                messages.error(request, 'Email already exist.')
                return redirect(request.path_info)
            user = MyUser.objects.create(email=email, username=username)
            user.set_password(password)
            user.save()
            token = Token.objects.create(user=user)
            current_site = get_current_site(request)
            print(current_site)
            message = render_to_string('account/send_otp.html', {
                'user': user,
                'domain': current_site.domain,
                'token': token,
            })
            email = EmailMessage(
                'Accoutn Activation email', message, to=[email]
            )
            email.send()
            messages.success(request, 'We have send you an activation email..')
            return redirect(request.path_info)
    elif request.method == "GET":
        return render(request, 'account/signup.html')
    
def AccountLogout(request):
    logout(request)
    return redirect('/')



    
def AccountActivate(request, id=None, token=None):
    if(request.user.is_authenticated):
        return redirect('/')
    if(request.method == 'GET'):
        try:
            token = Token.objects.get(token=token)
        except Token.DoesNotExist:
            messages.error(request, 'Token is not valid')
            return redirect('/')
        try:
            user = MyUser.objects.get(id=id)
        except MyUser.DoesNotExist:
            messages.error(request, 'User does not exist')
            return redirect('/')
        if(token.user == user):
            user.is_active = True
            user.save()
            token.delete()
            messages.success(request, 'Your account has been activated successfully')
            return redirect('/login/')