from django.db import models
from django.utils.translation import ugettext as _
from timezone_field import TimeZoneField
from common import enums
# Create your models here.

class Region(models.Model):
    # timezone = TimeZoneField(default='America/Merida')
    name = models.CharField(_("Title region"), max_length=50)
    currency = models.PositiveSmallIntegerField(
        choices=enums.Currency.choices(),
        verbose_name=_('currency user'),
        default=enums.Currency.MXN.value
    )
    
    def __str__(self):
        """
        Returns a string representation of this `Region`.

        This string is used when a `Region` is printed in the console.
        """
        return "{}".format(self.name)


    class Meta:
        verbose_name = 'Region'
        verbose_name_plural = 'Regions'



# class Currency(models.Model):
#     name = models.CharField(_("Title of charge"), max_length=50)
#     type = models.IntegerField(
#         choices=enums.Currency.choices(),
#         verbose_name=_('Charges currency money'),
#         default=enums.Currency.MXN.value
#     )
#     tax = models.IntegerField(default=0,verbose_name=_("Custom tax in percent"))