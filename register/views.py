from django.shortcuts import render,redirect

from django.contrib.auth.models import User

from django.contrib import auth

from django.contrib import messages

from django.views import generic
from django.shortcuts import render,get_object_or_404
from django.contrib.auth.views import PasswordResetCompleteView


class custom (PasswordResetCompleteView):

    success_url = '/register/login/'

def login(request):

    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:

            auth.login(request,user)
            return redirect("/")
        else:
            messages.error(request,'Invalid Credentials')
            return redirect(login)
    else:
        return render(request,'register/login.html')

def register(request):

    if request.method == 'POST':
        first_name = request.POST['First_name']
        last_name = request.POST['Last_name']
        username = request.POST['name']
        password1 = request.POST['password1']
        password2= request.POST['password2']
        email = request.POST['email']

        if password1 == password2:

            if User.objects.filter(username=username):
                messages.error(request,'Username already taken')
                return redirect('/register')
            
            elif User.objects.filter(email=email):
                messages.error(request,'Email already exists')
                return redirect('/register')

            else: 
                user = User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password1,email=email)
                user.save();
                messages.success(request,'User Created')
                return redirect(login)
                
        else:

            messages.error(request,'Password not matching')
            return redirect('/register')
    else:

        return render (request,'register/register.html')
    
def logout(request):

    auth.logout(request)
    return redirect('/')

# Create your views here.


   