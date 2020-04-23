from django.test import TestCase 
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL  = reverse('user:create')
TOKEN_URL =reverse('user:token')

def create_user(**params) : 
    return get_user_model().objects.create_user(**params)


class TestPublicUserApi(TestCase)  : 
    
    def setUp(self) : 
        self.client = APIClient()

    def test_create_valid_user(self) : 
        payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'testpass',
            'name' : 'test name'
        }
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code ,201)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password' , res.data)
    def test_create_user_already_exists (self) : 
        payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'testpass',
            'name' : 'test name'
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , 400)
    
    def test_create_with_short_password (self) : 
        payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : '@',
            'name' : 'test name'
        }
        res = self.client.post(CREATE_USER_URL , payload)
        self.assertEqual(res.status_code , 400)
        user_exists = get_user_model().objects.filter(
            email = payload['email']
        ).exists()
        self.assertFalse(user_exists)

        def test_create_token_for_user(self) : 
            payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'testpass'        }
            create_user(**payload)
            res =self.client.post(TOKEN_URL,payload)
            self.assertIn('token' , res.data)
            self.assertEqual(res.status_code , 200)
        
        def test_create_token_invalid_credentials(self) : 
            payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'testpass',
            'name' : 'test name'
        }
            create_user(**payload)
            payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'sdhfvdfh'
        }
            res =self.client.post(TOKEN_URL,payload)
            self.assertNotIn('token' , res.data)
            self.assertEqual(res.status_code , 400)
        
        def test_create_token_non_user(self) : 
            payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'sdhfvdfh'
        }
            res =self.client.post(TOKEN_URL,payload)
            self.assertNotIn('token' , res.data)
            self.assertEqual(res.status_code , 400)

        def test_create_token_missing_field(self) : 
            payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : 'testpass',
            'name' : 'test name'
        }
            create_user(**payload)
            payload = {
            'email' :'samacyc@gmail.com' , 
            'password' : ''
        }
            res =self.client.post(TOKEN_URL,payload)
            self.assertNotIn('token' , res.data)
            self.assertEqual(res.status_code , 400)

        



        
        