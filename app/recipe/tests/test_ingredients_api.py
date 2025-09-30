'''Tests for ingredients API'''

from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer

INGREDIENTS_URL=reverse('recipe:ingredient-list')



def detail_url(ingredient_id):
    '''create and return ingredients detail url'''

    return reverse('recipe:ingredient-detail', args=[ingredient_id])

def create_user(email='user2@eaxmple.com', password='test123'):
    '''create and return user'''
    return get_user_model().objects.create_user(email=email, password=password)


class PublicIngredientsApiTest(TestCase):
    '''Test unauthenticated Api request'''
    def setUp(self):
        self.client=APIClient()

    def test_auth_required(self):
        '''Test auth is required for retrieving ingredients'''

        res=self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)



class PrivateIngredientsApiTest(TestCase):
    '''test unauthenticated api requtest'''

    def setUp(self):
        self.user=create_user(email='test1@example.com', password='test123')

        self.client=APIClient()
        self.client.force_authenticate(self.user)


    def test_retrieve_ingredients(self):
        '''test retrieving ingredients'''
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='vanilla')
        res=self.client.get(INGREDIENTS_URL)
        ingredients=Ingredient.objects.all().order_by('-name')
        serializer=IngredientSerializer(ingredients, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


    def test_ingredients_limited_to_user(self):
        '''test ingredients limited to user'''
        user3=create_user(email='test@example.com')
        Ingredient.objects.create(user=user3, name='Strawberry')
        ingredient=Ingredient.objects.create(user=self.user, name='Any fruit')

        res=self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], ingredient.name)
        self.assertEqual(res.data[0]['id'], ingredient.id)


    def test_update_ingredient(self):
        '''test updatinng an ingredient'''
        ingredient=Ingredient.objects.create(user=self.user, name='lemon')
        payload={'name': 'Sour soup'}
        url=detail_url(ingredient.id)
        res=self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])


    def test_deleting_ingredient(self):
        '''test deleting ingredient'''
        ingredient=Ingredient.objects.create(user=self.user, name='Cocoa')
        url=detail_url(ingredient.id)
        res=self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredient=Ingredient.objects.filter(user=self.user)
        self.assertFalse(ingredient.exists())































