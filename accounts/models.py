from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils.crypto import get_random_string
from django.conf import settings
from datetime import datetime, timedelta
from django.utils.timezone import make_aware


class MyUserManager(BaseUserManager):
    
    def create_user(self, email, first_name, last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name='John', last_name='Doe', password=None):
        """
        Creates and saves a superuser with the given email, first_name, last_name and password.
        """
        user = self.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        'Does the user have a specific permission?'
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        'Does the user have permissions to view the app `app_label`?'
        # Simplest possible answer: Yes, always
        return True
    
    def is_token_valid(self, token):
        tok = self.tokens.filter(token=token).first()
        if tok:
            expiry = tok.created_at + timedelta(hours=int(settings.TOKEN_EXPIRY_HOURS))
            if expiry > make_aware(datetime.now()):
                return True

        return False

    @property
    def is_staff(self):
        'Is the user a member of staff?'
        return self.is_admin

def get_rand_token():
    return get_random_string(120)

class Token(models.Model):
    token = models.CharField(unique=True, max_length=255, default=get_rand_token)
    user = models.ForeignKey(User, related_name='tokens', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)