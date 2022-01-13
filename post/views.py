from django.shortcuts import render
from .models import Post
# Create your views here.

def view_posts(request):
    posts = Post.objects.all()
    context = {
        'posts': posts
    }
    return render(request, 'post/post.html', context)