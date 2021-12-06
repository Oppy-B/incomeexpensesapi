from django.db import models
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from rest_framework_simplejwt import tokens
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
# Create your models here.

class CustomUserManager(BaseUserManager): #To manage our custom model
    
    def create_user(self, username, email, password=None):
        if username is None:
            raise TypeError('Users should have a username')
            #print ('Enter a username')

        if email is None:
            raise TypeError('Users should have an email')
            #print ('Enter an email')

        user = self.model(username=username, email=self.normalize_email(email)) # Define how a user should be created
        user.set_password(password)
        user.save()
        return user

        def create_superuser(self, username, email, password=None): #create a super user
            if password is None:    
                raise TypeError('Password field should not be empty')
                #print ('Enter a username')  

            user = self.create_user(username, email, password)
            user.is_superuser = True
            user.is_staff = True
            user.save()
            return user

        

class User(AbstractBaseUser, PermissionsMixin):
     username = models.CharField(max_length=255, unique=True, db_index=True)
     email = models.EmailField(max_length=255, unique=True, db_index=True)
     is_verified = models.BooleanField(default=False) 
     is_active = models.BooleanField(default=True) 
     is_staff = models.BooleanField(default=False)   
     created_at = models.DateTimeField(auto_now_add=True)
     updated_at = models.DateTimeField(auto_now=True)

     USERNAME_FIELD = 'email' # This is the unique identifier that will be used for login instead of the django default username
     REQUIRED_FIELDS = ['username']

     objects = CustomUserManager()

     def __str__(self):
         return self.email

     def tokens(self):
         refresh = RefreshToken.for_user(self)          # contains both the refresh and access token
         return {
            'refresh': str(refresh),                    # When a user login in we give them their refresh and access token 
                                                        # And when their login expires we refresh it using their refresh token without logging out the user
            'access': str(refresh.access_token)          
        }


        

        


