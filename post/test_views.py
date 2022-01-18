from django.test import TestCase
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.models import User
from .models import Post

# Create your tests here.

class TestViews(TestCase):

    def test_get_index_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_get_post_detail_page(self):
        post = Post.objects.create(title="Test Recipe Post")
        response = self.client.get(reverse('post_detail', args=(post.slug,)))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'post_detail.html')
        

    def test_get_your_recipe_page(self):
        response = self.client.get('/your_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'your_recipes.html')

    # def test_get_add_recipe_page(self):

    # def test_get_edit_recipe_page(self):

    # def test_can_add_recipe(self):

    # def test_can_delete_recipe(self):

