from django.shortcuts import render , redirect
from django.http import HttpResponse
from .models import * 
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login , logout
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url="/login") #edirect unauthenticated users to the login page 
def receipes(request):
    if request.method == 'POST':
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')
        
        Receipe.objects.create(
            receipe_name=receipe_name,
            receipe_description = receipe_description,
            receipe_image = receipe_image)
        
    querySet = Receipe.objects.all()
    if request.GET.get('search'):
        querySet = querySet.filter(receipe_name__icontains=request.GET.get('search'))
    
    context = {'receipes': querySet}
    return render(request , "vege/receipes.html",context)


@login_required(login_url="/login") #edirect unauthenticated users to the login page 
def update_receipe(request,id):
    querySet = Receipe.objects.get(id=id)
    
    if request.method == 'POST':
        data = request.POST
        receipe_name = data.get('receipe_name')
        receipe_description = data.get('receipe_description')
        receipe_image = request.FILES.get('receipe_image')

        querySet.receipe_name = receipe_name
        querySet.receipe_description = receipe_description

        if receipe_image:
            querySet.receipe_image = receipe_image

        querySet.save()
        return redirect('/receipes/')
        
    print("id =" , querySet.id)
    print("name " , querySet.receipe_name )

    context = {'receipe': querySet}

    return render(request , "vege/update_receipe.html",context)

@login_required(login_url="/login") #edirect unauthenticated users to the login page 
def delete_receipe(request,id):
    querySet = Receipe.objects.get(id=id)
    querySet.delete()

    return redirect('/receipes/')


def logout_page(request):
    logout(request)
    return redirect('/login')

def login_page(request):
    if request.method == 'POST':
        data = request.POST
        username = data.get('username')
        password = data.get('password')

        if not User.objects.filter(username=username).exists():
            messages.info(request, ' invalid username')
            return redirect('/login')
        
        user =authenticate(username = username, password =password)

        if user is None:
            messages.info(request, ' invalid password')
            return redirect('/login')
        
        else:
            login(request , user)
            return redirect('/receipes/')


    return render(request, 'vege/login.html')

def register(request):
    if request.method == 'POST':
        data = request.POST
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        username = data.get('username')
        password = data.get('password')

        user = User.objects.filter(username = username)

        if user.exists():
            messages.info(request, 'username already taken')
            return redirect('/register')

        user = User.objects.create(
            first_name= first_name,
            last_name = last_name,
            username =  username,
            password = password)
        
        user.set_password(password)
        user.save()
        messages.info(request, 'user created successfully')

        return redirect('/register')
       
    return render(request, 'vege/register.html')