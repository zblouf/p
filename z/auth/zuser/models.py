from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from django.db import models
from django import forms
from django.contrib.auth.models import User, UserManager
from z.saas.models import Account

USER_TYPE_CHOICES = (
    ( 0, _("Standard")),
    (10, _("Retail")),
    (42, _("Superadmin")),
)

@python_2_unicode_compatible
class ZUser(models.Model):
    # User.username is prefixed by a 10 char hex representation of account_id
    #
    user = models.OneToOneField(User)
    user_type = models.PositiveIntegerField(default=0, choices=USER_TYPE_CHOICES)
    account = models.ForeignKey(Account, blank=True, null=True, default=None)
    is_admin = models.BooleanField(default=False)
    is_generic = models.BooleanField(default=False)
    generic_prefix = models.CharField(max_length=100, default='', blank=True)
    phone = models.CharField(max_length=100, blank=True, 
                    default="", verbose_name=_("phone number"))
    position = models.CharField(max_length=100, blank=True, 
                    default="", verbose_name=_("position/post"))
    comment = models.TextField(verbose_name=_("comment"), blank=True, 
                    default="")

#    objects = UserManager

    class Meta:
        verbose_name = _("Z user")

    def __str__(self):
        return '%s | %s' % (self.clean_username, self.account.login)
    
    @property
    def clean_username(self):
        if self.user.is_superuser:
            return self.user.username
        else:
            return self.user.username[10:]
    @property
    def display_name(self):
        if self.user.get_full_name()!="":
            return self.user.get_full_name()
        else:
            return "[ %s ]" %(self.clean_username)

    class Meta:
        ordering = ['user__username']


# 
# Forms
# 

class LoginForm(forms.Form):
    account = forms.SlugField(  label=_("account"), 
                                help_text=_("name of the account"))
    username = forms.CharField( max_length=20, 
                                initial="",
                                label=_("username"),
                                help_text=_("username"))
    password = forms.CharField( max_length=30, 
                                initial="", 
                                widget=forms.PasswordInput,
                                label=_("password"),
                                help_text=_("password"))

class LostPasswordForm(forms.Form):
    email = forms.EmailField(   initial="e-m@i.l",
                                label=_("email"))

class ProfileForm(forms.Form):
    first_name = forms.CharField(   max_length=50,
                                    initial="",
                                    label=_("first name"),
                                    help_text=_("first name"))
    last_name = forms.CharField(    max_length=50,
                                    initial="",
                                    label=_("last name"),
                                    help_text=_("last name"))
    email = forms.EmailField(   initial="",
                                label=_("email"),
                                help_text=_("email address"))
    position = forms.CharField( max_length=100,
                                label=_("position/post"),
                                help_text=_("position/post"))
    phone = forms.CharField(max_length=20,
                            label=_("phone number"),
                            help_text=_("phone number"))

