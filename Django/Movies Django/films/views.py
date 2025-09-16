from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Movie

def index(request):
    movies = Movie.objects.order_by('-rating')
    return render(request, 'index.html', {'movies': movies})

def add_movie(request):
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '').strip()
            description = request.POST.get('description', '').strip()
            rating = request.POST.get('rating', '0')
            
            if not all([title, description, rating]):
                raise ValidationError('All fields are required')
                
            rating = int(rating)
            if not (1 <= rating <= 10):
                raise ValidationError('Rating must be between 1 and 10')
                
            Movie.objects.create(
                title=title,
                description=description,
                rating=rating
            )
            return redirect('index')
            
        except (ValueError, ValidationError) as e:
            error_message = str(e)
            return render(request, 'add.html', {
                'error': error_message,
                'form_data': request.POST
            })
            
    return render(request, 'add.html')

def remove_movie(request, movie_id):
    try:
        movie = Movie.objects.get(id=movie_id)
        movie.delete()
        return redirect('index')
    except Movie.DoesNotExist:
        return render(request, 'error.html', {'message': 'Movie not found'})
