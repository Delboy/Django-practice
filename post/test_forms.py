from django.test import TestCase
from .forms import RecipeForm


class TestRecipeForm(TestCase):
    def test_recipe_name_is_required(self):
        form = RecipeForm({'title': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors.keys())
        
    def test_fields_are_explicit_in_form_metaclass(self):
        form = RecipeForm()
        self.assertEqual(form.Meta.fields, (
            'title', 
            'description', 
            'ingredients', 
            'method', 
            'is_vegan', 
            'image'
            )
            )

        