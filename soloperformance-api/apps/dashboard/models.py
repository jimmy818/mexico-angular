from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext as _
# Create your models here.
from apps.payments import models as plan_model
from uuid import uuid4
import os
from apps.security import models as user_model
from apps.teams import models as team_model

def path_and_rename(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'widget/'

    # return the whole path to the file
    return os.path.join(path, filename)


class Widget(models.Model):
    name = models.CharField(_("name widget"), max_length=150)
    image = models.ImageField(_("image widget"), upload_to=path_and_rename)
    min = models.IntegerField(
        _("Minumun size"),
        default=1,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ]
    )
    max = models.IntegerField(
        _("Maximun size"),
        default=12,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ]
    )
    resizable = models.BooleanField(_("Resizable"), default=True)

    class Meta:
        verbose_name = 'Widget'
        verbose_name_plural = 'Widgets'
        
    
    def __str__(self):
        """
        Returns a string representation of this `Widget`.

        This string is used when a `Widget` is printed in the console.
        """
        return "{}".format(self.name)
    
class Event(models.Model):
    name = models.CharField(_("name event"), max_length=150)
    hour_start = models.TimeField(_("Hour start"), auto_now=False, auto_now_add=False)   
    hour_end = models.TimeField(_("Hour end"), auto_now=False, auto_now_add=False)  
    date_start = models.DateField(_("Date start event"), auto_now=False, auto_now_add=False)
    date_end = models.DateField(_("Date end event"), auto_now=False, auto_now_add=False)
    team = models.ManyToManyField(
        team_model.Team, 
        verbose_name=_("Teams event"), 
        blank=True)
    athletes = models.ManyToManyField(
        'security.User', 
        verbose_name=_("Athletes events"),
        blank=True,
        related_name='event_athletes'
        )
    created_by = models.ForeignKey(
        "security.User",
        verbose_name=_("Created event user"),
        on_delete=models.SET_NULL,
        null=True,
        blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        
    
    def __str__(self):
        """
        Returns a string representation of this `Event`.

        This string is used when a `Event` is printed in the console.
        """
        return "{}".format(self.name)

class EventPoster(models.Model):
    name = models.CharField(_("name event"), max_length=150)
    date_start = models.DateField(_("Date start event"), auto_now=False, auto_now_add=False)
    date_end = models.DateField(_("Date end event"), auto_now=False, auto_now_add=False)
    team = models.ManyToManyField(
        team_model.Team, 
        verbose_name=_("Teams event"), 
        blank=True)
    athletes = models.ManyToManyField(
        'security.User', 
        verbose_name=_("Athletes events"),
        blank=True,
        related_name='event_poster_athletes'
        )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Event Poster'
        verbose_name_plural = 'Events Poster'
        
    
    def __str__(self):
        """
        Returns a string representation of this `Event`.

        This string is used when a `Event` is printed in the console.
        """
        return "{}".format(self.name)
    

class UserWidget(models.Model):
    user = models.ForeignKey(user_model.User, verbose_name=_("User widget"), on_delete=models.CASCADE,null=True,blank=True)
    widget = models.ForeignKey(Widget, verbose_name=_("Widget user"), on_delete=models.CASCADE)
    axis_x = models.IntegerField(_("Axis x"))
    axis_y = models.IntegerField(_("Axis y"))
    size = models.IntegerField(
        _("Size"),
        default=12,
        validators=[
            MaxValueValidator(12),
            MinValueValidator(1)
        ]
    )
    class Meta:
        verbose_name = 'User Widget'
        verbose_name_plural = 'Users Widget'
        
