from django.core.validators import RegexValidator

from django.db import models
from django.core.validators import MaxValueValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
    PermissionsMixin


alphanumeric = RegexValidator(r'^[0-9]*$', 'Doar caractere numerice sunt acceptate.')
cnp_length = RegexValidator(r'^.{13}$', 'Lungimea trebuie sa fie 13.')


class UserManager(BaseUserManager):
    def create_user(self, email, password, is_superuser=False, **extra_fields):
        user = self.model(
            email=email, is_active=True, is_superuser=is_superuser,
            **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_medic(self, email, password, **extra_fields):
        return self.create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        return self.create_user(
            email, password, is_superuser=True, **extra_fields)


class Specialization(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Prenume")
    last_name = models.CharField(max_length=40, null=True, blank=True, verbose_name="Nume")
    description = models.TextField(null=True, blank=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, null=True, blank=True, verbose_name="Numar telefon")
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, db_index=True)
    is_staff = models.BooleanField(default=True)
    is_patient = models.BooleanField(default=False)
    dob = models.PositiveIntegerField(validators=[MaxValueValidator(100)], null=True, blank=True, verbose_name="Varsta")
    cnp = models.CharField(max_length=13, null=True, blank=True, validators=[alphanumeric, cnp_length], unique=True)
    USERNAME_FIELD = 'email'
    objects = UserManager()

    class Meta:
        db_table = "user"
        verbose_name_plural = "users"
        unique_together = ['email', 'cnp']

    def __str__(self):
        return f"{self.name} - {self.specialization}"

    @property
    def name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.email
