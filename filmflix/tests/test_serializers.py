from rest_framework.test import APITestCase
from filmflix.models import CustomerUser, Icon, Video
from filmflix.serializers import CustomerUserSerializer, IconSerializer, VideoSerializer

class IconSerializerTest(APITestCase):
    
    def test_icon_serializer(self):
        icon = Icon.objects.create(name='Test Icon', image='icons/test_icon.png')
        serializer = IconSerializer(icon)
        self.assertEqual(serializer.data['name'], 'Test Icon')

class CustomerUserSerializerTest(APITestCase):
    
    def test_user_serializer(self):
        user = CustomerUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword123')
        serializer = CustomerUserSerializer(user)
        self.assertEqual(serializer.data['email'], 'test@example.com')

class VideoSerializerTest(APITestCase):

    def test_video_serializer(self):
        video = Video.objects.create(
            title='Test Video',
            description='Test description',
            videos_file='videos/test.mp4',
            thumbnail='thumbnails/test.png',
            sport='football',
            category='ballsport'
        )
        serializer = VideoSerializer(video)
        self.assertEqual(serializer.data['title'], 'Test Video')
