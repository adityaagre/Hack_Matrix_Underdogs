from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for Harmony.
    Further user types will have OneToOne relationships with this model.
    """

    class UserType(models.TextChoices):
        COMMUNITY = "COM"
        MEMBER = "MEM"

    username = models.CharField(_("Username"), max_length=150, unique=True)
    email = models.EmailField(_("Email address"), unique=True)
    password = models.CharField(_("Password"), max_length=255, blank=False, null=False)
    date_joined = models.DateTimeField(_("Date Joined"), auto_now_add=True)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)
    type = models.CharField(_("User Type"), max_length=3, choices=UserType.choices, default=UserType.MEMBER)
    first_name = None
    last_name = None
    # default fields
    is_active = models.BooleanField(_("Active Status"), default=True)
    is_staff = models.BooleanField(_("Staff Status"), default=False)
    is_superuser = models.BooleanField(_("Superuser Status"), default=False)

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Member(models.Model):
    """
    Model for a Member of Harmony.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(_("First Name"), max_length=30)
    last_name = models.CharField(_("Last Name"), max_length=30)
    prn_number = models.CharField(_("PRN Number"), max_length=10, blank=False, null=False)
    date_of_birth = models.DateField(_("Date of Birth"), blank=False, null=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name_plural = "members"
        verbose_name = "member"
        ordering = ["first_name"]


class Community(models.Model):
    """
    Model for a Community in Harmony.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(_("Community Name"), max_length=255, blank=False, null=False)
    description = models.TextField(_("Description"), blank=True, null=True)
    members = models.ManyToManyField(Member, related_name="communities", related_query_name="community")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "communities"
        verbose_name = "community"
        ordering = ["name"]
