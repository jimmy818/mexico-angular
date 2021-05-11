from django.contrib import admin
from . import models
# Register your models here.
class QuestionInline(admin.TabularInline):
    model = models.Question

@admin.register(models.Survey)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        QuestionInline,
    ]
    list_display = ('name',)


@admin.register(models.AnswerText)
class AnswerTextAdmin(admin.ModelAdmin):
    list_display = ('question',)