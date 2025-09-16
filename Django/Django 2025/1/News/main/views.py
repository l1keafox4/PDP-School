from django.http import HttpResponse
from main.models import Info, Contact
from django.shortcuts import render, redirect



def home(request):
    return render(request, 'news.html')
# Create your views here.

def contact(request):
    if request.method == 'CONTACT':
        first_name = request.CONTACT.get('firstname')
        last_name = request.CONTACT.get('lastname')
        country = request.CONTACT.get('country')
        subject = request.CONTACT.get('subject')

        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            country=country,
            subject=subject
        )
    # elif request.method == 'GET':
    #     context = {"form": ContactForm()}
    return render(request, 'contact.html')