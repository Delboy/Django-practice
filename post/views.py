from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from django.contrib import messages
from .models import Post
from .forms import CommentForm, RecipeForm
# Create your views here.


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(is_vegan=True)
    template_name = "index.html"
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.all()
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, 'SUCCESS! Comment accepted and awaiting approval')
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)

        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)
        
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))




def users_recipe_list(request):
    posts = Post.objects.filter(author=request.user)
    context = {
        "posts": posts
    }
    return render(request, 'your_recipes.html', context)



def add_recipes(request):
    if request.method == "POST":
        form = RecipeForm(request.POST or None)
        if form.is_valid():
            form.instance.author = request.user
            
            
            form.save()
        return redirect('add_recipes')
    form = RecipeForm()
    context = {
        'form': form
    }

    return render(request, 'add_recipe.html', context)


    # if request.method == "POST":
    #     form = RecipeForm(request.POST)
    #     if form.is_valid():
    #         recipe = form.save(commit=False)
    #         form.user = request.user
    #         form.save()
    #         return redirect('your_recipes.html')
    # else:
    #     form = RecipeForm()
    #     context = {
    #         'form': form
    #     }
    # return render(request, 'add_recipe.html', context)
