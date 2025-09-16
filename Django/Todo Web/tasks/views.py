from django.shortcuts import render, redirect
from .models import Task
from django.utils import timezone

def index(request):
    tasks = Task.objects.order_by('-important', '-created_at')
    return render(request, 'index.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        importance = request.POST.get('importance', 'medium')
        if title:
            Task.objects.create(title=title, important=importance)
    return redirect('index')

def delete_task(request, task_id):
    Task.objects.filter(id=task_id).delete()
    return redirect('index')

def mark_done(request, task_id):
    task = Task.objects.get(id=task_id)
    task.done = not task.done 
    task.save()
    return redirect('index')

def edit_task(request, task_id):
    task = Task.objects.get(id=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title', task.title)
        task.important = request.POST.get('importance', task.important)
        task.priority = request.POST.get('priority', task.priority)
        task.due_date = request.POST.get('due_date', task.due_date)
        task.save()
        return redirect('index')
    return render(request, 'edit.html', {'task': task})
