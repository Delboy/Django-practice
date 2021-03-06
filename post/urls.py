from . import views
from django.urls import path

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('recipes/', views.PostList.as_view(), name='recipes'),
    path('search_recipes/', views.search_recipes, name='search_recipes'),
    path('your_recipes/', views.UsersRecipeList.as_view(), name='your_recipes'),
    path('favourite_recipes/', views.UsersFavRecipes.as_view(), name='favourite_recipes'),
    path('add_recipes/', views.AddPostView.as_view(), name='add_recipes'),
    path('<slug:slug>/', views.PostDetail.as_view(), name="post_detail"),
    path('like/<slug:slug>', views.PostLike.as_view(), name="post_like"),
    path('edit_recipe/<int:pk>', views.UpdatePostView.as_view(), name="edit_recipe"),
    path('delete_recipe/<str:pk>', views.delete_recipe, name='delete_recipe'),
]