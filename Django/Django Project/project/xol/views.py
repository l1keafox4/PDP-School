from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView, ListView, DeleteView
# from .models import People
# Create your views here.

def Home(request):
    return render(request, 'FigmaProject.html')
