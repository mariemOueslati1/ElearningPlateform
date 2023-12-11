
from django.shortcuts import render

def acceuil_view(request):
    return render(request, 'acceuil/acceuil.html')
def contact_view(request):
    return render(request, 'acceuil/about2.html')
def about_view(request):
    return render(request, 'acceuil/about.html')
