
from django.template import loader
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import ugettext as _
from apps.payments import models as model_payment
from rest_framework import exceptions
from . import models
from rest_framework_simplejwt.tokens import RefreshToken


def send_reset_password_email_reset(user, site):
    token = user.activation_token
    reset_url = f'{site.domain}api/v1/reset-password/{token}/'
    html_message = loader.render_to_string('reset_password_email.html', {
        'activation_url': reset_url,
        'title': _('Reset password'),
        'message': _('Welcome to Solo Performance, click on the following link to recover password for you access account'),
        'link': _('If it does not redirect the button, copy the following link:'),
        'button_link': _('Go to link'),
        'team': _('team')
        
        })

    recipient_list = [user.email]
    send_mail(
        subject='Restablece tu contraseña',
        message='Restablece tu contraseña',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message
    )

def send_activation_email(user_email, activation_code, site):
    activation_url = f'{site.domain}api/v1/activate/{activation_code}/'
    html_message = loader.render_to_string('activation_email.html', {
        'activation_url': activation_url,
        'title': _('Active account'),
        'message': _('Welcome to Solo Performance, click on the following link to activate your account'),
        'link': _('If it does not redirect the button, copy the following link:'),
        'button_link': _('Go to link'),
        'team': _('team'),
        })
    recipient_list = [user_email]
    send_mail(
        subject=_('Código de activación'),
        message=_('Código de activación'),
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=recipient_list,
        fail_silently=False,
        html_message=html_message
    )
    
def validate_permissions(user,type_create):
    '''
    SUPER_ADMIN = 1
    INSTITUTION_MANAGER = 2
    STRENGTH_COACH = 3
    ATHLETE = 4    
    '''
    type_create = int(type_create)
    print(type_create,user.type)
    if user.type == 1:
        if type_create == 1 or type_create == 2:
            return True
    if user.type == 2:
        if type_create == 2:
            return True
        subscription = model_payment.Subscription.objects.filter(institution=user.institution,is_active=True).first()
        if not subscription:
            raise exceptions.ValidationError(_('you don´t have suscriptions actives'))
        elif type_create == 3:
            total_coach = models.User.objects.filter(
                institution=user.institution,
                type=3).count()
            if total_coach >= subscription.total_coaches:
                raise exceptions.ValidationError(_('this institution has limit of coaches created'))
            return True
        elif type_create == 4:
            total_coach = models.User.objects.filter(
                institution=user.institution,
                type=4).count()
            if total_coach >= subscription.total_athletes:
                raise exceptions.ValidationError(_('this institution has limit of athletes created'))
            return True
    if user.type == 3:
        if type_create == 4:
            return True
    return False


def validate_auth_media(email,type):
    user = models.User.objects.filter(email=email).first()
    if user:
        if user.social_type != type:
            raise exceptions.ValidationError(_('this email already register with another type authentication'))
        return True, user
    else:
        return False, None

def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'permission' : {
            'type': user.type,
            'str_type': user.get_type_display(),
        },
        'institution' : user.institution.id if user.institution else None
    }