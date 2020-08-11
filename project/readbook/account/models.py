from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class MyAccountManager(BaseUserManager):
    def create_user(self, username, email, password=None):
        if not username:
            raise ValueError("Users must have an username")
        if not email:
            raise ValueError("Users must have an email")
        
        user = self.model(
                username = username,
                email = self.normalize_email(email),
              )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self, username, email, password=None):
        user = self.create_user(
            username = username,
            password = password,
            email = self.normalize_email(email),
        )
        user.is_admin = True
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class Account(AbstractBaseUser):
    # 
    GENDER_CHOICES = (
          ('M', 'Male'),
          ('F', 'Female')
        )
    username      = models.CharField(verbose_name='Username',max_length = 30, unique = True)
    gender        = models.CharField(choices= GENDER_CHOICES ,max_length = 30)
    phone         = models.CharField(verbose_name='Phone', max_length = 20)
    email         = models.EmailField(max_length = 60, verbose_name = 'email', unique = True)
    uimg           = models.CharField(max_length=256,null=True)
    date_of_birth = models.CharField(verbose_name='birth_date',max_length=40)
    join_date     = models.DateTimeField(verbose_name='join_date', auto_now_add=True)
    last_login    = models.DateTimeField(verbose_name='last_login', auto_now=True)
    is_admin      = models.BooleanField(default=False)
    is_active     = models.BooleanField(default=True)
    is_superuser  = models.BooleanField(default=False)
    is_staff      = models.BooleanField(default=False)

    objects = MyAccountManager()

    USERNAME_FIELD  = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username
    
    def has_perm(self,perm,obj=None):
        return self.is_admin

    def has_module_perms(self, app_lebel):
        return True
