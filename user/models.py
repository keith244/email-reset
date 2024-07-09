from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager,PermissionsMixin
# Create your models here.

class myUserManager(BaseUserManager):
     def create_user(self,username,email,password=None, **extra_fields):
          if not username:
               raise ValueError('The username field must be included')
          if not email:
               raise ValueError('The email field must be provided')
          
          username = self.model.normalize_username(username)
          email    = self.normalize_email(email)

          extra_fields.pop('email', None)
          user  = self.model( username = username, email=email, **extra_fields )
          user.set_password(password)
          user.save( using = self._db )
          return user
     
     def create_superuser( self,username,email,password=None, **extra_fields ):
          extra_fields.setdefault( 'is_staff', True )
          extra_fields.setdefault( 'is_superuser',True)

          return self.create_user( username, email, password, **extra_fields )

class myUser(AbstractBaseUser,PermissionsMixin):
    username    = models.CharField( max_length = 255, unique=True ) 
    email       = models.EmailField( unique= True )
    is_staff    = models.BooleanField ( default=False ) 
    is_active   = models.BooleanField(default=True) 
    date_joined = models.DateTimeField(auto_now_add=True)  

    objects = myUserManager()

    USERNAME_FIELD  =  'username'
    REQUIRED_FIELDS =   ['email']

    def __str__(self):
         return self.username
    
    class Meta:
         verbose_name        = 'User'
         verbose_name_plural = 'Users'
