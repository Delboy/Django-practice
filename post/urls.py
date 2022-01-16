from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('your_recipes/', views.UsersRecipeList.as_view(), name='your_recipes'),
    path('add_recipes/', views.add_recipes, name='add_recipes'),
    path('<slug:slug>/', views.PostDetail.as_view(), name="post_detail"),
    path('like/<slug:slug>', views.PostLike.as_view(), name="post_like")
]