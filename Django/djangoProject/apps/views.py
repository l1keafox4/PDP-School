from django.http import HttpResponse
from apps.models import Post, Contact
from django.shortcuts import render, redirect





def home(request):
    return render(request, 'main/Home.html')
def news(request):
    data = {}
    data['dataset'] = Post.objects.all()
    return render(request, 'main/news.html', context=data)


def contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        country = request.POST.get('country')
        subject = request.POST.get('subject')

        Contact.objects.create(
            first_name=first_name,
            last_name=last_name,
            country=country,
            subject=subject
        )
    # elif request.method == 'GET':
    #     context = {"form": ContactForm()}
    return render(request, 'main/contact.html')
