from rest_framework import serializers
from .models import CustomerUser, Icon, Video
from django.contrib.auth import get_user_model

User = get_user_model()


class IconSerializer(serializers.ModelSerializer):
    class Meta:
        model = Icon
        fields = ['id', 'name', 'image']

    def get_image(self, obj):
        request = self.context.get('request')
        image_url = obj.image.url
        return request.build_absolute_uri(image_url) if request else image_url
    
    
class CustomerUserSerializer(serializers.ModelSerializer):

    icon = IconSerializer(read_only=True)
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'username', 'password', 'icon')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            username=validated_data.get('username'),
            password=validated_data['password'],
            # icon = icon
        )
        return user
    
class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

class ChangeNameSerializer(serializers.Serializer):
    new_name = serializers.CharField(required=True)
    new_firstname = serializers.CharField(required=True)
    new_lastname = serializers.CharField(required=True)
    new_icon = serializers.JSONField()  # Damit wird das neue Icon als JSON akzeptiert


