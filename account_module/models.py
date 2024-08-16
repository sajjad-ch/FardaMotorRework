from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class Persons(AbstractUser):
    username = models.CharField(primary_key=True, unique=True, verbose_name='کد پرسنلی', max_length=20)

    groups = models.ManyToManyField(
        Group,
        related_name='persons_set',  # Changed related_name to avoid clash
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='persons_set',  # Changed related_name to avoid clash
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return str(self.username)
