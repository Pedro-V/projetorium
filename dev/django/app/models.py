from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from .managers import UserManager

"""
class Departamento(models.Model):
    cod_departamento = models.CharField(max_length=10)
    nome = models.CharField(max_length=200)

class Professor(Pessoa):
    matricula_professor = models.CharField(primary_key=True, max_length=12)
    cod_departamento = models.ForeignKey(Departamento, on_delete=models.SET("Nao existe"))

class Projeto(models.Model):
    id_projeto = models.CharField(max_length=10)

class Proposta(models.Model):
    id_proposta = models.charField(10)
    matricula_professor = models.ForeignKey(Professor, on_delete=)
    id_projeto = models.ForeignKey(Projeto, on_delete=)
"""

# User base model, used for authentication in the system
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_admin = models.BooleanField(
        _('admin status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_student = models.BooleanField(
        _('student'),
        default=False,
        help_text=_('Designates whether the user is a student.')
    )
    is_teacher = models.BooleanField(
        _('teacher'),
        default=False,
        help_text=('Designates whether the user is a teacher.')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        '''
        Returns the first_name plus the last_name, with a space in between.
        '''
        return f'{self.first_name} {self.last_name}'

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.first_name

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
