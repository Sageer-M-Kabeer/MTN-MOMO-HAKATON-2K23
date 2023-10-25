from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField
from .attributes import Country,State,City,Gender
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.validators import RegexValidator
import phonenumbers 
from phonenumbers import carrier 
from .utils import generate_unique_pid
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.utils.html import mark_safe

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone_number,first_name,last_name, password=None, **extra_fields):
        if not phone_number:
            raise ValueError('The phone number must be set')
        if not email:
            raise ValueError('The email must be set')
        if not first_name:
            raise ValueError('The first name must be set')
        if not last_name:
            raise ValueError('The last name must be set')
        

        extra_fields.setdefault('is_active', True)

        # Check if the user exists based on the phone number
        existing_user = self.get_queryset().filter(phone_number=phone_number).first() or self.get_queryset().filter(email=email).first() 
        if existing_user:
            return existing_user

        user = self.model(email=email, phone_number=phone_number,first_name=first_name,last_name=last_name, **extra_fields)
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self,email, phone_number,first_name, last_name, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email,phone_number,first_name,last_name, password, **extra_fields)
   

class User(AbstractBaseUser,PermissionsMixin):
    phonenumber_regex = RegexValidator(regex=r'^\+\d{12}$')
    phone_number = models.CharField(max_length=15,unique=True,
                                validators=[phonenumber_regex], 
                                error_messages={'unique': ("A user with that phone number already exists."),},)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateField(auto_now_add=True)
    last_login = models.DateField(auto_now=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    other_name = models.CharField(max_length=25,blank=True)
    email = models.EmailField(unique=True)
    otp = models.CharField(max_length=6, null=True, blank=True)
    otp_verified = models.BooleanField(default=False)
    email_verified = models.BooleanField(default=False)
    phone_number_verified = models.BooleanField(default=False)

    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = CustomUserManager()

    def get_full_name(self):
        '''gets users's full name'''
        full_name = self.first_name + ' ' + self.last_name if self.other_name == "" else self.first_name + ' ' + self.last_name + ' ' + self.other_name
        return full_name
 
    def __str__(self):

        return f'{self.phone_number}'

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
    
    def validate_user_phone_number(self):
        #perse phone number
        phoneNumber = phonenumbers.parse(str(self.phone_number))
        # Getting carrier of a phone number 
        Carrier = carrier.name_for_number(phoneNumber, 'en')
        return Carrier

    
    @property
    def token(self):
        token = jwt.encode({"phone_number":self.phone_number,"exp":datetime.utcnow() + timedelta(hours=24)}
                           ,settings.SECRET_KEY,algorithm='HS256')
        
        return token



class Location(models.Model):
    country = models.CharField(max_length=10, choices=Country.choices)
    state = models.CharField(max_length=10, choices=State.choices)
    city = models.CharField(max_length=10, choices=City.choices)
    address = models.CharField(max_length=50)

    def __str__(self) -> str:
        return f'{self.country}:{self.state}:{self.city}'

class Profile(models.Model):

    username_validator = UnicodeUsernameValidator()

    profile_id = models.CharField(max_length=16,default="",blank=True,editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    username = models.CharField(max_length=25,unique=True,validators=[username_validator])
    profile_picture = models.ImageField(upload_to="",blank=True,null=True)
    gender = models.CharField(max_length=1,choices=Gender.choices,default="")
    positive_feedback = models.PositiveIntegerField(null=True, editable=False)
    negative_feedback = models.PositiveIntegerField(null=True, editable=False)
    is_varified = models.BooleanField(default=False)
    # ratings = models.PositiveIntegerField(def editable=False)

    def __str__(self) -> str:
        return f'{self.username}'
    
    def is_verified(self):
        return f'Verified: {self.is_varified}'
    
    def save(self,*args, **kwargs):
        code = generate_unique_pid()
        
        if not Profile.objects.filter(profile_id=code).exists():
            self.profile_id = code
        super(Profile,self).save(*args, **kwargs)
        
    def profile_picture_tag(self):
        return mark_safe('<img src="%s" width="50px" height="50px" style="border-radius:8px" />' %(self.profile_picture.url))
    profile_picture_tag.short_description = 'Picture'