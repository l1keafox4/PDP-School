from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DeleteView
from .models import *
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Contact
from .forms import *
from django.urls import reverse_lazy

class ContactListView(ListView):
    model = Contact
    template_name = 'contacts/contact_list.html'
    context_object_name = 'contacts'

class ContactCreateView(CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact_list')

class ContactUpdateView(UpdateView):
    model = Contact
    form_class = ContactForm
    template_name = 'contacts/contact_form.html'
    success_url = reverse_lazy('contact_list')

class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contacts/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')
class Contact(ListView):
    model = Contact
    context_object_name = 'contacts'
    template_name = 'contacts.html'