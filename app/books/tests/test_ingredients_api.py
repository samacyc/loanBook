from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from core.models import Ingredients
from books.serializers import IngredientSerializer


INGREDIENT_URL =reverse('books:ingredients-list')

class PublicTestApiIng(TestCase) : 
    def setUp(self) : 
        self.client = APIClient()
    
    def test_login_required(self) : 
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code , 401)

class PrivateTestApiIng(TestCase) : 
    def setUp(self) : 
        self.user = get_user_model().objects.create_user(
            email = 'test@python.com' , password = 'testpass'
        )
        self.client = APIClient()
        self.client.force_authenticate(user = self.user)
    
    def test_retrieve_ingredients(self) : 
        Ingredients.objects.create(user = self.user , name = 'dgfvbj')
        Ingredients.objects.create(user = self.user , name = 'svjnj')
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code , 200)
        ings = Ingredients.objects.all().order_by('-name')
        serlizer = IngredientSerializer(ings , many = True) 
        self.assertEqual(res.data , serlizer.data)
    
    def test_ings_limited_user(self) : 
        user2 = get_user_model().objects.create_user(
            email = 'samacyc@python.com' , password = 'testpassword'
        )
        Ingredients.objects.create(user=user2 , name = 'sdjf' )
        ingredients =  Ingredients.objects.create(user=self.user , name = 'sjvgbbhjb' )
        res = self.client.get(INGREDIENT_URL)
        self.assertEqual(res.status_code , 200)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'] , ingredients.name) 

        
        #Ingredients        
    def test_create_ingredients(self) : 
        payload = {
            'name' :'gfhgj', 
            'user' : self.user
        }
        
        res = self.client.post(INGREDIENT_URL , payload)
        self.assertEqual(res.status_code , 201)
        ing_exist = Ingredients.objects.filter(user = self.user , name = payload['name']).exists()
        self.assertTrue(ing_exist)
    def test_create_invalid_ing (self) : 
        payload = {
            'name' : ''
        }
        res = self.client.post(INGREDIENT_URL , payload)
        self.assertEqual(res.status_code , 400)