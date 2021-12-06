from django.shortcuts import render
from rest_framework import generics, serializers,status,views
from .serializers import RegisterSerializer,EmailVerificationSerilizer,LoginSerializer,ResetPasswordEmailRequestSerializer,SetNewPasswordSerializer

from rest_framework.response import Response
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Utils
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .renderers import UserRenderer

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,smart_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import Utils
from django.urls import reverse
# Create your views here.

class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer #declaring the serializer class to pass the data to
    renderer_classes = (UserRenderer,)
    
    def post(self,request):
        user = request.data
        serializer=self.serializer_class(data=user) #pass the data to the serializer class
        serializer.is_valid(raise_exception=True)  #Run a method validate in serializer.py to validate the data
        serializer.save() #run a method create in serializer.py to create

        user_data = serializer.data
        user = User.objects.get(email=user_data['email']) # Getting the current email of the newly validated user

        #token = RefreshToken.for_user(user)
        token = RefreshToken.for_user(user).access_token # to get the access token b user id

        relativeLink = reverse('email-verify')
        current_site = get_current_site(request).domain # get the current site of the registration url
        absurl = 'http://'+current_site+relativeLink+'?token='+ str(token)

        email_body = 'Hi ' + user.username + ' click on the link below to verify your email \n' + absurl
        data = {'email_body': email_body, 'to_email' : user.email, 'email_subject':'Verify your Email'}

        Utils.send_email(data) # instantiated instantly because we declared a static method in the util class
        

        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerilizer # to expose the token field

    token_param_config= openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING
    )

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token','') # to get the token assigned in the email sent to the user for verification
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"]) #decode the token using our secret key to give us the data encoded in our token
            user = User.objects.get(id=payload['user_id']) # get the user that was encoded in our token by id, jwt works with a key called user_id which we use to get the user ID
            if not user.is_verified:
                user.is_verified = True
                user.save()
            return Response({'email':'Successfully activated'}, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError as identifier:
            return Response({'error':'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
           return Response({'error':'invalid token'}, status.HTTP_400_BAD_REQUEST)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK) # return back our data after the serializer have validated the data

class ResetPasswordEmailRequest(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email','')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))                     # ENCODING THE USER ID
            token = PasswordResetTokenGenerator().make_token(user)      # CREATE A PASSWORD RESET TOKEN FOR THE USER AND ENSURE IT CAN'T BE USED AGAIN AFTER IT'S BEEN USED ONCE TO GENERATE ANOTHER PASSWORD
            
            current_site = get_current_site(request=request).domain # get the current site of the registration url
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token': token})
            absurl = 'http://'+current_site + relativeLink

            email_body = 'Hello \n click on the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email' : user.email, 'email_subject':'Reset your Password'}

            Utils.send_email(data) # instantiated instantly because we declared a static method in the util class

        return Response({'success': 'we have sent you a link to reset your password'}, status=status.HTTP_200_OK)

class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self,request, uidb64, token, *args, **kwargs):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64)) #NOTE:: DECODE THE UIB64
            user = User.objects.get(id=id)                   # GET THE USER ID FROM DECODED UIDB64

            if not PasswordResetTokenGenerator().check_token(user, token): #NOTE :: CHEC IF TOKEN HAS BEEN USED BY USER BEFORE i,e if not flase TOKEN HAS BEEN USED
                return Response({'error': 'Token is not valid, please request a new one'}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({'success':True, 'message': 'Credential Valid', 'uidb64': uidb64, 'token':token}, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:                      # IF USER TAMPERED WITH THE TOKEN
            return Response({'error': 'Token is not valid, Please request a new one'})

class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message': 'password reset success'}, status=status.HTTP_200_OK)