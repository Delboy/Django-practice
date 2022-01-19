from django.test import TestCase
from .models import Post


class TestModels(TestCase):

    def test_is_vegan_defaults_to_false(self):
        post = Post.objects.create(title='Test is Vegan post')
        self.assertFalse(post.is_vegan)