from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.test import TestCase
from rest_framework import status
from filmflix.models import Icon, Video
from filmflix.token import account_activation_token

User = get_user_model()

class RegisterViewTest(APITestCase):
    
    def test_register_user(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)        
        
        
    def test_register_user_without_email(self):
        url = reverse('register')
        data = {
            'username': 'testuser',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)
        
    
    def test_register_user_without_username(self):
        url = reverse('register')
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123',
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('error', response.data)    
    

    def test_register_user_with_invalid_icon(self):
        url = reverse('register')
        data = {
            "email": "test@example.com",
            "password": "Test1234!",
            "icon": {
                "id": 9999,  # Ein ungültiges Icon, das nicht existiert
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 400)
        
class ActivationViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='testpassword',
            is_active=False
        )
        self.token = account_activation_token.make_token(self.user)
        self.uidb64 = urlsafe_base64_encode(force_bytes(self.user.pk))

    # def test_activation_with_valid_params(self):
    #     response = self.client.get(reverse('activate', kwargs={'uidb64': self.uidb64, 'token': self.token}))
    #     self.user.refresh_from_db()  # Refresh the user instance from the database
    #     self.assertTrue(self.user.is_active)
    #     self.assertRedirects(response, f'http://localhost:4200/confirm/{self.user.pk}')

    def test_activation_with_invalid_token(self):
        invalid_token = 'invalid_token'
        response = self.client.get(reverse('activate', kwargs={'uidb64': self.uidb64, 'token': invalid_token}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Activation link is invalid!')

    def test_activation_with_non_existent_user(self):
        invalid_uidb64 = urlsafe_base64_encode(force_bytes(999))  # Non-existent user ID
        response = self.client.get(reverse('activate', kwargs={'uidb64': invalid_uidb64, 'token': self.token}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Activation link is invalid!')
        

class LoginViewTest(APITestCase):

    def setUp(self):
        # Erstelle Icon und User
        self.icon = Icon.objects.create(name="Test Icon", image="icon.png")
        self.user = User.objects.create_user(username="testuser", email="testuser@example.com", password="testpassword", icon=self.icon)
        self.url = reverse('login')  

    # def test_login_success(self):
    #     data = {
    #         'username': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     response = self.client.post(self.url, data)
        
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('token', response.data)
    #     self.assertEqual(response.data['user_id'], self.user.id)
    #     self.assertEqual(response.data['username'], self.user.username)
    #     self.assertEqual(response.data['icon']['id'], self.icon.id)

    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # def test_token_created_on_login(self):
        
    #     data = {
    #         'username': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     response = self.client.post(self.url, data)
        
    #     token = Token.objects.get(user=self.user)
    #     print(token)
    #     self.assertEqual(response.data['token'], token.key)

    # def test_token_reused_on_login(self):
    
    #     token = Token.objects.create(user=self.user)
    #     print(token)
        
    #     data = {
    #         'username': 'testuser',
    #         'password': 'testpassword'
    #     }
    #     response = self.client.post(self.url, data)
        
    #     self.assertEqual(response.data['token'], token.key)
    


class VideoViewTest(APITestCase):
    
    def test_video_list(self):
        url = reverse('video')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_video_creation(self):
        url = reverse('video')
        
        data = {
            'new_title': 'Test Video',
            'new_description': 'Test description',
            'new_video': 'videos/test.mp4',
            'new_thumbnail': 'thumbnails/test.png',
            'sport': 'football',
            'category': 'ballsport'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    
    def test_delete_video(self):
        video = Video.objects.create(
            title='Test Video',
            description='Test description',
            videos_file='videos/test.mp4',
            thumbnail='thumbnails/test.png',
            sport='football',
            category='ballsport'
        )
        url = reverse('single_video', args=[video.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        
    def setUp(self):
        self.url = reverse('video_choices')  
    
    def test_video_choices_view(self):
        
        response = self.client.get(self.url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)        
        self.assertIn('sport_choices', response.data)
        self.assertIn('category_choices', response.data)
        self.assertEqual(response.data['sport_choices'], Video.SPORT_CHOICES)
        self.assertEqual(response.data['category_choices'], Video.CATEGORY_CHOICES)


class IconViewsTest(APITestCase):
    
    def setUp(self):
        self.icon1 = Icon.objects.create(name='Icon 1', image='icon1.png') 
        self.icon2 = Icon.objects.create(name='Icon 2', image='icon2.png')  
        self.icon_list_url = reverse('icon-list')  
        self.icon_detail_url = reverse('icon-detail', args=[self.icon1.pk])  

    def test_icon_list_view(self):
        
        response = self.client.get(self.icon_list_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], self.icon1.name)
        self.assertEqual(response.data[1]['name'], self.icon2.name)

    def test_icon_detail_view(self):
        response = self.client.get(self.icon_detail_url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.icon1.name)

    def test_icon_detail_view_not_found(self):
        response = self.client.get(reverse('icon-detail', args=[999]))  # 999 ist eine nicht existierende ID
        
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'Icon not found')
        

class ChangeNameViewTest(APITestCase):
    
    def setUp(self):
        # Erstelle einen Benutzer und ein Icon für Tests
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            first_name='Test',
            last_name='User'
        )
        self.icon = Icon.objects.create(name='Test Icon', image='test_icon.png')  # Füge hier weitere Felder hinzu
        self.user.icon = self.icon
        self.user.save()

        self.url = reverse('change-name', args=[self.user.pk])  # Ersetze 'change-name' mit dem tatsächlichen URL-Namen

    def test_change_name_success(self):
        data = {
            'new_name': 'new_username',
            'new_firstname': 'NewFirstName',
            'new_lastname': 'NewLastName',
            'new_icon': {
                'id': self.icon.id
            }
        }
        
        response = self.client.put(self.url, data, format='json')
        
        # Überprüfe den Statuscode
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Überprüfe, ob die Änderungen gespeichert wurden
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'new_username')
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.last_name, 'NewLastName')
        self.assertEqual(self.user.icon, self.icon)

    def test_change_name_user_not_found(self):
        # Teste die Änderung des Namens für einen nicht vorhandenen Benutzer
        url = reverse('change-name', args=[999])  # 999 ist eine nicht existierende ID
        data = {
            'new_name': 'new_username',
            'new_firstname': 'NewFirstName',
            'new_lastname': 'NewLastName',
            'new_icon': {
                'id': self.icon.id
            }
        }
        
        response = self.client.put(url, data, format='json')
        
        # Überprüfe den Statuscode
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')

    def test_change_name_invalid_icon(self):
        # Teste die Änderung des Namens mit einem ungültigen Icon
        data = {
            'new_name': 'new_username',
            'new_firstname': 'NewFirstName',
            'new_lastname': 'NewLastName',
            'new_icon': {
                'id': 999  # Ungültige ID
            }
        }
        
        response = self.client.put(self.url, data, format='json')
        
        # Überprüfe den Statuscode
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
