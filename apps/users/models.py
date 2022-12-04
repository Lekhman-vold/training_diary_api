from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.core import validators


def upload_handler(instance, filename):
    return f'usersFiles/{instance.id}/avatars/' \
           f'{timezone.now().timestamp()}_{filename}'


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser):
    email = models.EmailField(_('email'),
                              max_length=254,
                              unique=True,
                              db_index=True,
                              null=True,
                              help_text=_('Required. 254 characters or fewer. '
                                          'Letters, digits and @/./+/-/_ only.'),
                              validators=[
                                  validators.RegexValidator(
                                      r'^[\w.@+-]+$',
                                      _('Enter a valid username. This value may contain only '
                                        'letters, numbers ' 'and @/./+/-/_ characters.')
                                  ),
                              ],
                              error_messages={
                                  'unique': _("A user with that username already exists."),
                              },
                              )
    first_name = models.CharField(_('first name'), max_length=30, null=True, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, null=True, blank=True)
    birthday = models.DateField(_('birthday'), null=True, blank=True)
    avatar = models.ImageField(_('avatar'), upload_to=upload_handler, null=True, blank=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_email_verified = models.BooleanField(_('is_email_verified'), default=False)
    is_notifications = models.BooleanField(_('is notifications'),
                                           default=True)
    MALE = 0
    FEMALE = 1
    NONE = 2
    STATUS_CHOICES = (
        (MALE, 'Male'),
        (FEMALE, 'Female'),
        (NONE, 'None'),
    )
    gender = models.PositiveIntegerField(
        default=FEMALE,
        choices=STATUS_CHOICES)
    age = models.CharField(max_length=25, null=True, blank=True)
    last_password_changing = models.DateTimeField(_('Last password changing'),
                                                  null=True,
                                                  blank=True
                                                  )
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_superuser = models.BooleanField(_('superuser status'), default=False)

    def validate_password(self, password):
        if len(password) < 8:
            raise ValidationError(
                _("Password must have at least 8 characters"))

    @property
    def is_verified(self):
        return self.is_email_verified

    date_joined = models.DateField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        if self.email:
            return self.email

    class Meta:
        db_table = 'users'
        ordering = ['-date_joined']

    def forgot_password(self):
        pass

    def reset_password(self):
        pass

    def change_role(self, role):
        pass

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser
