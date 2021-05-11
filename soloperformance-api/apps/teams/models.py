from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.
from apps.payments import models as plan_model
from apps.security import models as user_model
from uuid import uuid4
import os


def path_and_rename(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'teams/'

    # return the whole path to the file
    return os.path.join(path, filename)


class Team(models.Model):
    name = models.CharField(_("Name team"), max_length=50)
    image = models.ImageField(_("image team"), upload_to=path_and_rename,null=True,blank=True)
    active = models.BooleanField(_("institution active"), default=True)
    updated_by = models.ForeignKey(
        "security.User",
        verbose_name=_("Last updated"),
        on_delete=models.SET_NULL,
        related_name='team_updated_by',
        null=True,
        blank=True)
    institution = models.ForeignKey(
        'Institution', 
        verbose_name=_("institution created"), 
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    institution_managers = models.ManyToManyField(
        'security.User', 
        verbose_name=_("Institution managers of team"),
        blank=True,
        related_name='team_institution_managers'
        )
    athletes = models.ManyToManyField(
        'security.User', 
        verbose_name=_("Athletes of team"),
        blank=True,
        related_name='team_athletes'
        )
    coaches = models.ManyToManyField(
        'security.User', 
        verbose_name=_("Coaches of team"),
        blank=True,
        related_name='team_coaches')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        
    
    def __str__(self):
        """
        Returns a string representation of this `Region`.

        This string is used when a `Region` is printed in the console.
        """
        return "{}".format(self.name)


class Institution(models.Model):
    name = models.CharField(_("Name team"), max_length=50)
    identifier_name = models.CharField(_("Name team"), max_length=250,unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    revenue = models.DecimalField(
        _("total revenue"), 
        max_digits=5, 
        decimal_places=2,
        default=0.00
        )
    active = models.BooleanField(_("institution active"), default=False)

    class Meta:
        verbose_name = 'Institution'
        verbose_name_plural = 'Institutions'
        
    
    def __str__(self):
        """
        Returns a string representation of this `Region`.

        This string is used when a `Region` is printed in the console.
        """
        return "{}".format(self.name)