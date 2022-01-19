from django.test import TestCase
from django.shortcuts import reverse
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

    def test_get_add_recipe_page(self):
        response = self.client.get('/add_recipes/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_recipes.html')


    def test_get_edit_recipe_page(self):
        post = Post.objects.create(title="Test Recipe Post")
        response = self.client.get(f'/edit_recipe/{post.id}')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_recipe.html')

    def test_can_add_recipe(self):
        response = self.client.post('/add_recipes/', {'title': 'Test Added Recipe'})
        self.assertEquals(response.status_code, 200)

    def test_can_delete_recipe(self):
        post = Post.objects.create(title="Test Recipe Post")
        response = self.client.get(f'/delete_recipe/{post.id}')
        self.assertRedirects(response, '/your_recipes/')
        existing_items = Post.objects.filter(id=post.id)
        self.assertEqual(len(existing_items), 0)


    def test_can_edit_recipe(self):
        post = Post.objects.create(title="Test Recipe Post", is_vegan=True)
        response = self.client.get(f'/edit_recipe/{post.id}')
        self.assertEquals(response.status_code, 200)
        updated_item = Post.objects.get(id=post.id)
        self.assertTrue(updated_item.is_vegan)
