import json
from django.shortcuts import redirect, render
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from filmflix.models import Icon, Video
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse, JsonResponse   
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage, send_mail
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from filmflix.serializers import ChangeNameSerializer, ChangePasswordSerializer, CustomerUserSerializer, IconSerializer, VideoSerializer

User = get_user_model()

def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
        user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()  
        return redirect(f'https://sportflix.naueka.de/#/confirm/{uid}') 
    else:  
        return HttpResponse('Activation link is invalid!') 


class RegisterView(APIView):
    
    def post(self, request, format=None):  
        try:
            
            email = request.data.get('email')
            if not email:
                return Response({'error': 'Email is required'}, status=400)
            
            username = request.data.get('username')
            if not username:
                return Response({'error': 'Username is required'}, status=400) 
        
            icon_data = request.data.get("icon")
            icon_id = icon_data.get('id') if icon_data else None

            if icon_id:
                try:
                    icon_instance = Icon.objects.get(id=icon_id)  # Icon-Instanz abrufen
                except Icon.DoesNotExist:
                    return JsonResponse({'error': 'Icon not found'}, status=400)
            else:
                icon_instance = None
            
            user = User.objects.create_user(username=request.data.get('username'),
                                            email=request.data.get('email'),
                                            password=request.data.get('password'),
                                            icon=icon_instance)
            user.is_active = False  
            user.save()            
          
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'link Sportflix'  
            try:
                print("Rendering email template")
                message = render_to_string('acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token': account_activation_token.make_token(user),  
                })
                
            except Exception as e:
                print(f"Error rendering email template: {str(e)}")
                return JsonResponse({'error': f'Email template error: {str(e)}'}, status=500)   
            
            email = EmailMessage(  
            mail_subject, message, to=[user.email]  
            )  
            email.send()
            
            return Response({'message': 'Please confirm your email address'}, status=200) 
    
        except Exception as e:
            print(f"Error during registration: {str(e)}")  # Detaillierte Fehlermeldung drucken
            return JsonResponse({'error': str(e)}, status=500) 
        

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user    
        user_serializer = CustomerUserSerializer(user)
        return Response(user_serializer.data)

class LoginView(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            
            # Icon-Serializer, wenn das Benutzer-Icon existiert
            icon_serializer = IconSerializer(user.icon) if user.icon else None
            
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
                'icon': icon_serializer.data if icon_serializer else None
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)               
     

class VideoView(APIView):    
    # Authentication with token
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
        
    
    def post(self, request):
        data = request.data
        video_file = data.get('new_video')
        thumbnail_file = data.get('new_thumbnail')
        video = Video(
            title=data.get('new_title'),
            description=data.get('new_description'),
            videos_file=video_file,
            thumbnail=thumbnail_file,
            sport=request.data.get('sport', ''),  
            category=request.data.get('category', None)  
        )
        
        video.save()

        return Response({
            "message": "Video erfolgreich hochgeladen",
            "video_id": video.id
        }, status=status.HTTP_201_CREATED)
        
    
    def delete(self, request, pk, format=None):
        try:
            video = Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        video.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class VideoChoicesView(APIView):
    def get(self, request):
        sport_choices = Video.SPORT_CHOICES
        category_choices = Video.CATEGORY_CHOICES
        
        return Response({
            "sport_choices": sport_choices,
            "category_choices": category_choices
        }, status=status.HTTP_200_OK) 
    

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



@method_decorator(csrf_exempt, name='dispatch')
class CustomPasswordResetView(APIView):
    def post(self, request):
        
        data = json.loads(request.body)
        email = data.get('email')         
        
        if not email:
            return JsonResponse({'error': 'Email is required'}, status=400)

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User with this email does not exist'}, status=404)

        # Generate password reset token and UID
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        reset_url = f'https://sportflix.naueka.de/setnewpassword/{uid}/{token}'

        mail_subject = 'Password Reset Requested'
        message = f'Click the link to reset your password: {reset_url}'
        email = EmailMessage(  
            mail_subject, message, to=[email]  
            )
        email.send() 

        return JsonResponse({'status': 'Password reset email sent successfully'})


@method_decorator(csrf_exempt, name='dispatch')
class CustomPasswordResetConfirmView(APIView):
    def post(self, request, uidb64, token):       
        
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            
            data = json.loads(request.body)
            new_password1 = data.get('new_password1')
            new_password2 = data.get('new_password2')

            if new_password1 and new_password1 == new_password2:
                user.set_password(new_password1)
                user.save()
                return JsonResponse({'status': 'Password has been reset successfully'})
            else:
                return JsonResponse({'error': 'Passwords do not match'}, status=400)
        else:
            return JsonResponse({'error': 'Invalid token or user ID'}, status=400)  

class ChangeName(APIView):
    
    def put(self, request, pk):
        
        serializer = self.validate_data(request.data)
        if not serializer:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        new_name, new_first_name, new_last_name, new_icon_data = self.extract_validated_data(serializer)
        user = self.get_user(pk)
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        self.update_user_data(user, new_name, new_first_name, new_last_name)
       
        icon = self.get_or_create_icon(new_icon_data)
        if not icon:
            return Response(IconSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user.icon = icon
        user.save()

        return Response({'success': 'Name and Icon updated successfully'}, status=status.HTTP_200_OK)
    
    def validate_data(self, data):
        serializer = ChangeNameSerializer(data=data)
        if serializer.is_valid():
            return serializer
        return None
    
    def extract_validated_data(self, serializer):
        new_name = serializer.validated_data['new_name']
        new_first_name = serializer.validated_data['new_firstname']
        new_last_name = serializer.validated_data['new_lastname']
        new_icon_data = serializer.validated_data['new_icon']
        return new_name, new_first_name, new_last_name, new_icon_data
    
    def get_user(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
    
    def update_user_data(self, user, new_name, new_first_name, new_last_name):
        user.username = new_name
        user.first_name = new_first_name
        user.last_name = new_last_name
    
    def get_or_create_icon(self, new_icon_data):
        try:
            return Icon.objects.get(id=new_icon_data['id'])
        except Icon.DoesNotExist:
            icon_serializer = IconSerializer(data=new_icon_data)
            if icon_serializer.is_valid():
                return icon_serializer.save()
        return None


    


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
    


  

