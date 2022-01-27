from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.views import generic, View
from django.views.generic import CreateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Count
from .models import Post
from .forms import CommentForm, RecipeForm

# Create your views here.

class HomeView(generic.ListView):
    def get(self, request):
        posts = Post.objects.filter(is_vegan=True)
        top_posts = Post.objects.annotate(like_count=Count('likes')).order_by('-like_count')
        paginate_by = 6
        context = {
            "posts": posts,
            "top_posts": top_posts,
        }
        return render(request, 'index.html', context)

class PostList(generic.ListView):
    model = Post
    template_name = "recipes.html"
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


class UsersFavRecipes(generic.ListView):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.filter(likes=request.user.id)
            
            context = {
                "posts": posts,
            }
            paginate_by = 6
            return render(request, 'favourite_recipes.html', context)
        else:
            
            return render(request, 'favourite_recipes.html')


class UsersRecipeList(generic.ListView):
    def get(self, request):
        if request.user.is_authenticated:
            posts = Post.objects.filter(author=request.user)
            context = {
                "posts": posts,
            }
            paginate_by = 6
            return render(request, 'your_recipes.html', context)
        else:
            
            return render(request, 'your_recipes.html')


<<<<<<< HEAD
class UsersFavRecipes(generic.ListView):
    def get(self, request):
        posts = Post.objects.filter(likes=request.user.id)
        context = {
            "posts": posts,
        }
        paginate_by = 6
        return render(request, 'favourite_recipes.html', context)
       





=======
>>>>>>> 13f1fb817a1cf55e6c2b1658686b3abdf4b180d6
class AddPostView(CreateView):
    model = Post
    form_class = RecipeForm
    template_name = 'add_recipes.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    
class UpdatePostView(UpdateView):
    model = Post
    template_name = 'edit_recipe.html'
    form_class = RecipeForm

    
def delete_recipe(request, pk):

    recipe = get_object_or_404(Post, id=pk)
    recipe.delete()

    return redirect(reverse('your_recipes'))


def search_recipes(request):
    if request.method == "POST":
        searched = request.POST.get('searched')
        posts = Post.objects.filter(title__contains=searched)
        return render(request, 'search_recipes.html', {'searched': searched, 'posts':posts})
    else:
        return render(request, 'search_recipes.html')


def top_recipes(request):
    post = Post.objects.filter(liked=False)
    context = {
        post: 'post',
        author: 'author'
    }
    return render(request, 'top_recipes.html', context)