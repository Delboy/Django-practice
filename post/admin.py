from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


@admin.register(Post)
class PostAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'is_vegan', 'published_on')
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('published_on', 'is_vegan')
    
    summernote_fields = ('description', 'ingredients', 'method')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):

    list_display = ('name', 'body', 'post', 'created_on', 'approved')
    search_fields = ('name', 'email', 'body')
    list_filter = ('approved', 'created_on')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)