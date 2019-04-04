from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser,
                                        PermissionsMixin)

import time
from datetime import datetime, timedelta


class UserManager(BaseUserManager):

    def _create_user(self, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser, last_login=now,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def create_user_profile(self, email, password=None, **extra_fields):
        return self._create_user(email, password, False, False,
                                 **extra_fields)

    def _create_user_profile(self, data, is_active=False):
        """
        Create a new user and its associated ``UserProfile``.
        Also, send user account activation (verification) email.
        """

        password = data.pop('password')
        user = User(**data)
        user.is_active = is_active
        user.set_password(password)
        user.save()

        user_profile = self.create_profile(user)

        return user

    def create_profile(self, user):
        """
        Create UserProfile for give user.
        Returns created user profile on success.
        """
        from profiles.models import Profile, Matchmaker, AdminProfile
        profile_model = None
        if user.is_single:
            profile_model = Profile
        if user.is_matchmaker:
            profile_model = Matchmaker
        if profile_model:
            created, profile = profile_model.objects.get_or_create(
                user=user
            )
            return profile
        return None

    def create_superuser(self, email, password, **extra_fields):
        return self._create_user(email, password, True, True,
                                 **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """ Represents the logged in user """

    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('email address'), blank=True, null=True, max_length=100)
    mobile = models.CharField(_('Mobile'), max_length=12, blank=True, default="")
    first_name = models.CharField(_('First name'), max_length=50, blank=True, default="")
    last_name = models.CharField(_('Last name'), max_length=50, blank=True, default="")
    is_staff = models.BooleanField(
        _('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(
        _('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)


    is_single = models.BooleanField(
        _('Single'), default=True)

    is_matchmaker = models.BooleanField(
        _('Mathcmaker'), default=False)

    is_admin = models.BooleanField(
        _('Admin'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.get_first_name(), self.get_last_name())
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user."""
        return self.first_name


    def get_first_name(self):
        """
        Return correct first name, depend user role
        """
        profile = self
        if self.is_single:
            profile = self.profile_set.first()
            return profile.firstName if profile else ""

        if self.is_matchmaker:
            profile = self.matchmaker_set.first()
            return profile.firstName if profile else ""
        return profile.first_name if profile else ""

    def get_last_name(self):
        """
        Return correct first name, depend user role
        """
        profile = self
        if self.is_single:
            profile = self.profile_set.first()
            return profile.lastName if profile else ""

        if self.is_matchmaker:
            profile = self.matchmaker_set.first()
            return profile.lastName if profile else ""
        return profile.last_name if profile else ""

    @property
    def single_id(self):
        """
        Returns profile id og single user
        """
        if self.is_single:
            return self.profile_set.first().id if self.profile_set.first() else None
        return None

    @property
    def matchmaker_id(self):
        """
        Returns profile id og single user
        """
        if self.is_matchmaker:
            return self.matchmaker_set.first().id if self.matchmaker_set.first() else None
        return None


ROLE_TYPES = (
    (1, _("Single")),
    (2, _("Matchmaker")),
)
