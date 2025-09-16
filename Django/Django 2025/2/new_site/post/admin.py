from django.contrib import admin
from .models import Category, Post
from django import forms
from ckeditor.widgets import CKEditorWidget

class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    list_display = ['id', 'title', 'slug', 'author', 'status']
    list_filter = ['status','created_date','published_date','author']
    search_fields = ['title', 'body', 'id']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'published_date'
    ordering = ['status', 'published_date']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'parent', 'slug', 'is_active']
    search_fields = ['name', 'slug', 'id']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_active',]