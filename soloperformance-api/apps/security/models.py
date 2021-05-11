from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import BooleanField
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core import signing
import os
import datetime
from common import enums
import uuid
from apps.regions import models as region_model
from apps.teams import models as team_model
from urllib import request
from django.core.files import File

# Create your models here.
def path_and_rename(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'users/{}/profile/'.format(obj.email)

    # return the whole path to the file
    return os.path.join(path, filename)

class User(AbstractUser):
    USER_TYPE = (
        (enums.UserRole.SUPER_ADMIN.value, _('Super Admin')),
        (enums.UserRole.INSTITUTION_MANAGER.value, _('Institution Manager')),
        (enums.UserRole.STRENGTH_COACH.value, _('Strength Coach')),
        (enums.UserRole.ATHLETE.value, _('Athlete')),
    )
    METRIC = (
        (1, _('English')),
        (2, _('International'))
    )
    SOCIAL_TYPE = (
        (1, _('Facebook')),
        (2, _('Google')),
        (3, _('Apple')),
        (4, _('Default')),
    )
    LANGUAJE = (
        (1, _('English')),
        (2, _('Spanish'))
    )
    type = models.IntegerField(
        choices=USER_TYPE,
        verbose_name=_('Rol'),
        default=enums.UserRole.STRENGTH_COACH.value
    )
    social_type = models.IntegerField(
        choices=SOCIAL_TYPE,
        verbose_name=_('Social Login Type'),
        default=4
    )
    token_social_login = models.TextField(
        null=True,
        blank=True
    )
    automatic_training = models.BooleanField(
        _("Training automatic enabled"),
        default=False)
    metric_system = models.IntegerField(
        choices=METRIC,
        verbose_name=_('System Metric'),
        default=2
    )
    languaje = models.IntegerField(
        choices=LANGUAJE,
        verbose_name=_('Languaje'),
        default=2
    )
    institution = models.ForeignKey(
        team_model.Institution, 
        verbose_name=_("institution"), 
        on_delete=models.CASCADE,
        blank=True, 
        null=True,
        )
    region = models.ForeignKey(
        region_model.Region, 
        blank=True, 
        null=True,
        verbose_name=_("Region user"), 
        on_delete=models.SET_NULL
        )
    full_name = models.CharField(
        max_length=255
        )
    country_code = models.PositiveSmallIntegerField(
        _("code country"),
        blank=True, 
        null=True,
        )
    phone = models.CharField(
        max_length=15,
        blank=True, 
        null=True,
        )
    last_edited = models.ForeignKey(
       'User', 
       verbose_name=_("last user edit this user"), 
       on_delete=models.SET_NULL,
       blank=True, 
       null=True,)
    weigth = models.DecimalField(_("weigth user (kg)"), max_digits=5, decimal_places=2,default=0.0)
    heigth = models.DecimalField(_("heigth user (m)"), max_digits=5, decimal_places=2,default=0.0)
    FCM = models.PositiveSmallIntegerField(_("maximum heart rate (bpm)"),default=0)
    MSS = models.DecimalField(_("Maximal Sprinting Speed (km/h)"), max_digits=5, decimal_places=2,default=0.0)
    MAS = models.DecimalField(_("Maximal Aerobic Speed (km/h)" ), max_digits=5, decimal_places=2,default=0.0)
    gender = models.PositiveSmallIntegerField(
        choices=enums.Gender.choices(),
        verbose_name=_('Rol'),
        default=enums.Gender.OTHER.value
    )
    birthday = models.DateField(
        _("Date Birthday"),
        auto_now=False, 
        blank=True, 
        null=True,
        auto_now_add=False
        )
    photo = models.ImageField(
        upload_to=path_and_rename,
        verbose_name=_('photo profile'),
        blank=True, 
        null=True,
    )
    email = models.EmailField(
        max_length=255, 
        unique=True
        )
    username = models.CharField(
        max_length=255
        )
    email_verified = models.BooleanField(
        verbose_name=_('email verified?'),
        default=False
    )
    deleted_widget = models.BooleanField(
        verbose_name=_('email verified?'),
        default=False
    )
    activation_token = models.UUIDField(
        default=uuid.uuid4
        )
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        auto_now=True
        )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'type', 'full_name']

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return "{} - {}".format(self.full_name, self.email)

    def display_name(self):
        """
        This method is required by Django for things like handling emails.
        Typically this would be the user's first and last name. Since we do
        not store the user's real name, we return their username instead.
        """
        return '{}'.format(self.full_name)

    def save_remote_image(self, remote_url):
        result = request.urlretrieve(remote_url)
        extension = result[1]['Content-Type'].split('/')[1]
        self.photo.save(
            f'{self.pk}.{extension}',
            File(open(result[0], 'rb'))
        )
        self.save()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
