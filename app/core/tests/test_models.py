from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models

def sample_user(email = 'test@python.com' , password = 'testpass') : 

    return get_user_model().objects.create_user(email , password)

class ModelTests(TestCase) : 
    
    def test_create_user_with_email_successful(self) : 
        email = 'test@samacyc.com'
        password = 'testpass'
        user = get_user_model().objects.create_user(
            email =email , 
            password = password
        )

        self.assertEqual(user.email , email)
        self.assertTrue(user.check_password(password))
    
    def test_new_user_email_normalized(self) : 

        email = 'test@SAMACYC.com'
        user = get_user_model().objects.create_user(email , 'testpass')

        self.assertEqual(user.email , email.lower())
    def test_new_user_invalid_email(self) : 

        with self.assertRaises(ValueError) :
            get_user_model().objects.create_user(None , 'ffdhbj')
    
    def test_create_new_superuser(self) : 
        user = get_user_model().objects.create_superuser(
            'test@samacyc.com', 
            'skjfvngjb'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str (self) : 
        tag = models.Tag.objects.create(
            user =sample_user() ,
            name = 'Vegen'
        )
        self.assertEqual(str(tag) , tag.name)
        