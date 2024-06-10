from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from filmflix.models import Video
from django.contrib.auth import get_user_model

from filmflix.serializers import VideoSerializer

User = get_user_model()
class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
            
        })       
        

class RegisterView(APIView):
    
    def post(self, request, format=None):
        try:
            user = User.objects.create_user(username=request.data.get('username'),
                                    email=request.data.get('email'),
                                    password=request.data.get('password'))
            token, created = Token.objects.get_or_create(user=user)        
            
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email
            })
            
        except:
            return 
        
        

class VideoView(APIView):    
    #Authentication with token
    # permission only when authentication is successful
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk:
            try:
                video = Video.objects.get(pk=pk)
            except Video.DoesNotExist:
                return Response(status=status.HTTP_404_NOT_FOUND)
            serializer = VideoSerializer(video)
            return Response(serializer.data)
        else:
            video = Video.objects.all()
            serializer = VideoSerializer(video, many=True)
            return Response(serializer.data)
    
    # def post(self, request, format=None):
    #     serializer = TaskPOSTSerializer(data=request.data)
    #     if serializer.is_valid():
    #             serializer.save()          
    #             return Response(serializer.data)
    #     return Response(serializer.errors)
    
    # def put(self, request, pk, format=None):
    #     try:
    #         task = Video.objects.get(pk=pk)
    #     except Video.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)
        
    #     serializer = TaskPOSTSerializer(task, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
