from django.db import models
from django.utils.translation import ugettext as _
from uuid import uuid4
import os
from common import enums
from apps.security import models as model_user
from apps.teams import models as model_team
# Create your models here.

def path_and_rename(obj, filename):
    ext = filename.split('.')[-1]
    # get filename
    # set filename as random string
    filename = '{}.{}'.format(uuid4().hex, ext)

    path = 'products/suscriptions/'

    # return the whole path to the file
    return os.path.join(path, filename)


class Subscription(models.Model):
    institution = models.ForeignKey(
        model_team.Institution, 
        verbose_name=_("institution"), 
        on_delete=models.CASCADE,
        null=True,
        blank=True)
    type = models.PositiveSmallIntegerField(
        choices=enums.TypeSubcription.choices(),
        verbose_name=_('type subscription'),
        default=enums.TypeSubcription.DEMOS.value
    )
    ends = models.DateField(_("ends suscription"), auto_now=False, auto_now_add=False)
    is_active = models.BooleanField(_("active subscription"),default=True)
    total_athletes = models.PositiveSmallIntegerField(_("number of athletes"))
    total_coaches = models.PositiveSmallIntegerField(_("number of coaches"))
    total_team = models.PositiveSmallIntegerField(_("number of teams"))
    price = models.DecimalField(_("price payed of subscription in dollars"), max_digits=6, decimal_places=2, default=0.0)
    tax = models.DecimalField(_("tax payed of subscription in dollars"), max_digits=6, decimal_places=2, default=0.0)
    fee_stripe = models.DecimalField(_("fee of stripe of subscription in dollars"), max_digits=6, decimal_places=2, default=0.0)
    total = models.DecimalField(_("total payed of subscription in dollars"), max_digits=6, decimal_places=2, default=0.0)
    has_renewable = models.BooleanField(_("renewable subscription"),default=False)
    created_at = models.DateTimeField(
        auto_now_add=True
        )
    updated_at = models.DateTimeField(
        auto_now=True
        )
    
    class Meta:
        verbose_name = 'Subscription'
        verbose_name_plural = 'Subscriptions'