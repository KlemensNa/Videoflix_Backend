from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics
from filmflix.models import Icon, Video
from django.contrib.auth import get_user_model

from django.http import HttpResponse, JsonResponse   
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import force_bytes, force_str  
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User  
from django.core.mail import EmailMessage  

from filmflix.serializers import ChangeNameSerializer, ChangePasswordSerializer, CustomerUserSerializer, IconSerializer, VideoSerializer

User = get_user_model()


# def signup(request):  
#     if request.method == 'POST':  
#         form = SignupForm(request.POST)  
#         if form.is_valid():  
#             # save form in the memory not in database  
#             user = form.save(commit=False)  
#             user.is_active = False  
#             user.save()  
#             # to get the domain of the current site  
#             current_site = get_current_site(request)  
#             mail_subject = 'Activation link has been sent to your email id'  
#             message = render_to_string('acc_active_email.html', {  
#                 'user': user,  
#                 'domain': current_site.domain,  
#                 'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
#                 'token':account_activation_token.make_token(user),  
#             })  
#             to_email = form.cleaned_data.get('email')  
#             email = EmailMessage(  
#                         mail_subject, message, to=[to_email]  
#             )  
#             email.send()  
#             return HttpResponse('Please confirm your email address to complete the registration')  
#     else:  
#         form = SignupForm()  
#     return render(request, 'signup.html', {'form': form}) 


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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')  
    else:  
        return HttpResponse('Activation link is invalid!') 


class RegisterView(APIView):
    
    # def post(self, request, format=None):
    #     try:
    #         user = User.objects.create_user(username=request.data.get('username'),
    #                                         email=request.data.get('email'),
    #                                         password=request.data.get('password'),
    #                                         icon=request.data.get("icon"))
    
    #             user.is_active = False  
    #             user.save()  
    #         token, created = Token.objects.get_or_create(user=user)            
    #         icon_serializer = IconSerializer(user.icon)  
            
    #         return Response({
    #             'token': token.key,
    #             'username': user.username,
    #             'email': user.email,
    #             'icon': icon_serializer.data
    #         })
            
    #     except:
    #         return 
    
    def post(self, request, format=None):  
        try:
            print("hello", request.data)
            
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
            print(user)
            user.is_active = False  
            user.save()
            
          
            # to get the domain of the current site  
            current_site = get_current_site(request)  
            print(current_site)
            mail_subject = 'Activation link has been sent to your email id'  
            try:
                print("Rendering email template")
                message = render_to_string('acc_active_email.html', {  
                    'user': user,  
                    'domain': current_site.domain,  
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
                    'token': account_activation_token.make_token(user),  
                })
                print("Email template rendered successfully")
            except Exception as e:
                print(f"Error rendering email template: {str(e)}")
                return JsonResponse({'error': f'Email template error: {str(e)}'}, status=500)   
            
            email = EmailMessage(  
            mail_subject, message, to=[user.email]  
            )  
            email.send()
            
            return HttpResponse('Please confirm your email address to complete the registration')  
    
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
            new_first_name = serializer.validated_data['new_firstname']
            new_last_name = serializer.validated_data['new_lastname']
            
            try:
                user = User.objects.get(pk=pk)
            except User.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
            
            user.username = new_name
            user.first_name = new_first_name
            user.last_name = new_last_name
            
            print(user)
            
            try:
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
    


  

