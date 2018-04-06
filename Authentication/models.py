from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.db import models


class AccountManager(BaseUserManager):
    def create_user(self, email, username, mobile, password=None, **kwargs):
        if not email:
            raise ValueError("email must be provided")
        if not username:
            raise ValueError("users must have a valid username")
        if not mobile:
            raise ValueError("Users must have a valid mobile number"
                             "in format +19999999999")

        account = self.model(
            email=self.normalize_email(email),
            username=username,
            mobile=mobile,
            first_name=kwargs.get('first_name', "first_name"),
            last_name=kwargs.get('last_name', "last_name"),

        )

        account.set_password(password)
        account.save()
        return account

    def create_superuser(self, email, username, mobile, password=None):
        account = self.create_user(
            email,
            username,
            mobile,
            password,
        )

        account.is_staff = True
        account.is_superuser = True
        account.save()
        return account


class Account(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{8,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    mobile = models.CharField(primary_key=True, validators=[phone_regex], unique=True, max_length=15)
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=50, default=mobile)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = AccountManager()

    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['username', 'email']

    def __str__(self):
        return "@{}".format(self.username)

    def get_short_name(self):
        return self.first_name

    def get_long_name(self):
        return "{ (@{})".format(self.last_name, self.mobile)
