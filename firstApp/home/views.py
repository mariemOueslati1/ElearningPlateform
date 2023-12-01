from django.shortcuts import render

from django.http import HttpResponse

def home(request):
    peoples = [
        {"name":"John" , "age":16 },
        {"name":"james" , "age":27}
    ]
    return render(request,"home/index.html",context={"peoples":peoples})

def about(request):
    context = {"page":"about"}
    return render(request,"home/about.html",context)

def contact(request):
    context = {"page":"contact"}
    return render(request,"home/contact.html",context)

def sucess(request):
    return HttpResponse("sucees")
