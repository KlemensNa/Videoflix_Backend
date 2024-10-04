from django.test import TestCase
from filmflix.models import Icon, CustomerUser, Video
from datetime import date

class IconModelTest(TestCase):
    
    def test_icon_creation(self):
        icon = Icon.objects.create(name='Test Icon', image='icons/test_icon.png')
        self.assertEqual(icon.name, 'Test Icon')
        self.assertTrue(icon.image.name.endswith('test_icon.png'))

class CustomerUserModelTest(TestCase):
    
    def test_user_creation(self):
        user = CustomerUser.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpassword123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword123'))

class VideoModelTest(TestCase):

    def test_video_creation(self):
        video = Video.objects.create(
            title='Test Video',
            description='Test description',
            created_at=date.today(),
            videos_file='videos/test.mp4',
            thumbnail='thumbnails/test.png',
            sport='football',
            category='ballsport'
        )
        self.assertEqual(video.title, 'Test Video')
        self.assertEqual(video.sport, 'football')
