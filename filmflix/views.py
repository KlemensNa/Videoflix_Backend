from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from django.contrib.auth import get_user_model

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
