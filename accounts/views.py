from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from contactss.models import Contact


def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(
                        request, 'email is taken before = ایمیل از قبل وجود دارد')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        first_name=first_name, last_name=last_name, email=email, password=password, username=username)
                    auth.login(request, user)
                    messages.success(request, 'register successfull')
                    return redirect('index')

                    # user.save()
                    # messages.success(request, 'ok')
                    # return redirect('login')
        else:
            messages.error(request, 'passwords are not matched')
            return redirect('register')
    else:
        return render(request,  'accounts/register.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'ok')
            return redirect('dashboard')
        else:
            messages.error(request, 'valid info')
            return redirect('login')
    else:
        return render(request,  'accounts/login.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'logout is ok')
        return redirect('index')


def dashboard(request):
    user_contacts = Contact.objects.order_by(
        '-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request,  'accounts/dashboard.html', context)
