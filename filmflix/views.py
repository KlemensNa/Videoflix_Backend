from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from filmflix.models import Icon, Video
from django.contrib.auth import get_user_model

from filmflix.serializers import ChangeNameSerializer, ChangePasswordSerializer, CustomerUserSerializer, IconSerializer, VideoSerializer

User = get_user_model()


class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user    
        user_serializer = CustomerUserSerializer(user)
        print(user_serializer.data)
        return Response(user_serializer.data)

class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        print(user)
        
        icon_serializer = IconSerializer(user.icon)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,   
            'icon': icon_serializer.data         
        })       
        

class RegisterView(APIView):
    
    def post(self, request, format=None):
        try:
            user = User.objects.create_user(username=request.data.get('username'),
                                            email=request.data.get('email'),
                                            password=request.data.get('password'),
                                            icon=request.data.get("icon"))
            token, created = Token.objects.get_or_create(user=user)
            
            icon_serializer = IconSerializer(user.icon)    
            
            return Response({
                'token': token.key,
                'username': user.username,
                'email': user.email,
                'icon': icon_serializer.data
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
    
    

class ChangePassword(APIView):
    serializer_class = ChangePasswordSerializer

    def put(self, request, pk):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']

            try:
                obj = get_user_model().objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=404)

            if not obj.check_password(password):
                return Response({'error': 'Old password does not match'}, status=400)

            obj.set_password(new_password)
            obj.save()
            return Response({'success': 'Password changed successfully'}, status=200)
        return Response(serializer.errors, status=400)
    
    

class ChangeName(APIView):

    def put(self, request, pk):
        serializer = ChangeNameSerializer(data=request.data)
        
        if serializer.is_valid():
            new_name = serializer.validated_data['new_name']
            new_icon_data = serializer.validated_data['new_icon']
            
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            # Update the user's name
            user.username = new_name

            # Update the user's icon
            try:
                # Versuche das Icon anhand der ID zu finden und zuzuweisen
                icon = Icon.objects.get(id=new_icon_data['id'])
            except Icon.DoesNotExist:
                # Falls das Icon nicht existiert, erstelle ein neues
                icon_serializer = IconSerializer(data=new_icon_data)
                print(icon_serializer)
                if icon_serializer.is_valid():
                    icon = icon_serializer.save()
                else:
                    return Response(icon_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            print(icon)
            user.icon = icon
            user.save()

            return Response({'success': 'Name and Icon updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    


class IconListView(generics.ListAPIView):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer
    

class IconView(generics.RetrieveAPIView):
    queryset = Icon.objects.all()
    serializer_class = IconSerializer

    def get(self, request, pk=None):
        try:
            icon = Icon.objects.get(pk=pk)
        except Icon.DoesNotExist:
            return Response({'error': 'Icon not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = IconSerializer(icon, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
