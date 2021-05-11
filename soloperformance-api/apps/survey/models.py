from django.db import models

from common import enums
from django.utils.translation import ugettext as _
from apps.catalog import models as model_catalog
from apps.security import models as model_user
# Create your models here.

class Survey(models.Model):
    SURVEY_TYPES = (
        (enums.TypeSurvey.PRE.value, _('pre-training')),
        (enums.TypeSurvey.POST.value, _('post-training')),
    )
    name = models.CharField(max_length=250)
    desciption = models.CharField(max_length=250,null=True,blank=True)
    survey_type = models.PositiveSmallIntegerField(choices=SURVEY_TYPES,default=enums.TypeSurvey.PRE.value)

    
    class Meta:
        verbose_name = 'Survey'
        verbose_name_plural = 'Survey'
    
class Question(models.Model):
    QUESTION_TYPES = (
        (enums.TypeQuestion.TEXT.value, _('text')),
        (enums.TypeQuestion.INTEGER.value, _('integer')),
        (enums.TypeQuestion.TIME.value, _('time')),
    )
    required = models.BooleanField(default=True)
    text = models.TextField()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    question_type = models.PositiveSmallIntegerField(choices=QUESTION_TYPES,default=enums.TypeQuestion.TEXT.value)
    class Meta:
            verbose_name = 'Question'
            verbose_name_plural = 'Questions'

class AnswerBase(models.Model):
	workout = models.ForeignKey(model_catalog.Workout, on_delete=models.CASCADE)
	user = models.ForeignKey(model_user.User, on_delete=models.CASCADE,null=True,blank=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)

class AnswerText(AnswerBase):
	response = models.CharField(max_length=50)


