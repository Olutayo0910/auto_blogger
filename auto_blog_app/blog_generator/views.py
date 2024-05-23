from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')

def user_login(request):
    return render(request, 'login.html')

def user_signup(request):
    return render(request, 'sign_up.html')

def user_logout(request):
    pass

