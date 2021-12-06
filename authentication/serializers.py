from django.http import request
from rest_framework import generics, serializers
from .models import User
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed

'''
#NOTE:: MOVED TO VIEWS.PY
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,smart_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from .utils import Utils
from django.urls import reverse
'''

from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str,smart_bytes,force_str,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=68, min_length=6, write_only=True)

    class Meta:
        model=User
        fields = ['email', 'username','password']   

    def validate(self, attrs): #attrs her should be the dictionary
        email = attrs.get('email', '')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError("The username should only contain Alphanumeric character")

        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
        
class EmailVerificationSerilizer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model= User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=3) #Declaring the fields we need for our login
    password = serializers.CharField(max_length=68, min_length=6, write_only=True)
    username = serializers.CharField(max_length=255, min_length=6, read_only=True)
    tokens = serializers.CharField(max_length=70, min_length=6, read_only=True)

    class Meta:
        model = User
        fields = ['email','password','username','tokens']

    def validate(self, attrs):
        email = attrs.get('email', '')                          # getting the email data 
        password = attrs.get('password', '')                    # getting the email data 

        user = auth.authenticate(email=email, password=password) # authenticate the user login credentails

        if not user:                                             # this condition should come first to avoid NONETYPE error from other conditions that will break your code 
            raise AuthenticationFailed('Invalid credentials, try again')

        if not user.is_active:
            raise AuthenticationFailed('Account disabled contact admin')

        if not user.is_verified:
            raise AuthenticationFailed('Email is not verifieid')

        
        return{
            'email' : user.email,
            'username': user.username,
            'tokens': user.tokens
        }
        return super().validate(attrs)

class ResetPasswordEmailRequestSerializer(serializers.Serializer): #make sure this inherit from Serializer instead of ModelSerializer to avoid Metamodel error
    email = serializers.EmailField(min_length=2)
    class Meta:
        fields = ['email']


    # NOTE :: CODE FOR VALIDATION BELOW MOVED TO VIEWS.PY BECAUSE WE COULD NOT ACCESS THE EMAIL DATA USER PROVIDED
    '''
    def validate(self, attrs):
        
        email = attrs.get('data','')             # GETTING THE DATA KEY(i.e request.data) FROM THE DICTIONARY DATA PASSED TO THE SERIALIZER CLASS IN THE 
        email1 = email['email']
        if User.objects.filter(email=email1).exists():
            user = User.objects.get(email=email1)
            uidb64 = urlsafe_base64_encode(user.id)                     # ENCODING THE USER ID
            token = PasswordResetTokenGenerator().make_token(user)      # CREATE A PASSWORD RESET TOKEN FOR THE USER AND ENSURE IT CAN'T BE USED AGAIN AFTER IT'S BEEN USED ONCE TO GENERATE ANOTHER PASSWORD
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64':uidb64, 'token': token})
            current_site = get_current_site(request=attrs['data'].get(request)).domain # get the current site of the registration url
            absurl = 'http://'+current_site+relativeLink

            email_body = 'Hello \n click on the link below to verify your email \n' + absurl
            data = {'email_body': email_body, 'to_email' : user.email, 'email_subject':'Reset your Password'}

            Utils.send_email(data) # instantiated instantly because we declared a static method in the util class

            return attrs
    '''


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
    uidb64 = serializers.CharField(min_length=1,write_only=True)

    class Meta:
        fields=['password','token','uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            token = attrs.get('token')
            uidb64 = attrs.get('uidb64')
            id = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator.check_token(user, token):
                raise AuthenticationFailed('The reset link is invalid', 401)

            user.set_password(password)
            user.save()

            return(user)
        except Exception as e:
            raise AuthenticationFailed('The reset link is invalid', 401)
        return super().validate(attrs)
