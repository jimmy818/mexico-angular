from rest_framework import serializers
from apps.teams import models as team_model
from . import models
from django.utils.translation import ugettext as _

class TeamField(serializers.Field):
    def to_representation(self, value):
        request = self.context.get('request')
        if value:
            image = request.build_absolute_uri(value.image.url) if value.image else None
            return { "id": value.id, "name": value.name, "image": image }
        return None

    def to_internal_value(self, data):
        try:
            return team_model.Team.objects.get(pk=data)
        except team_model.Team.DoesNotExist:
            raise serializers.ValidationError(_("Team does not exit."))


class CodingField(serializers.Field):
    def to_representation(self, value):        
        request = self.context.get('request')
        if value and request:
            icon = request.build_absolute_uri(value.icon.url) if value.icon else None
            return { "id": value.id, "name": value.name, "icon": icon }
        return None

    def to_internal_value(self, data):
        try:
            return models.Coding.objects.get(pk=data)
        except models.Coding.DoesNotExist:
            raise None


class CodingCategoryField(serializers.Field):
    def to_representation(self, value):
        if value:
            return { "id": value.id, "name": value.name }
        return None

    def to_internal_value(self, data):
        try:
            return models.CodingCategory.objects.get(pk=data)
        except models.CodingCategory.DoesNotExist:
            raise serializers.ValidationError(_("CodingCategory does not exit."))


class TypeField(serializers.Field):
    def to_representation(self, value):
        if value:
            return { "id": value.id, "name": value.name }
        return None

    def to_internal_value(self, data):
        try:
            return models.BlockType.objects.get(pk=data)
        except models.BlockType.DoesNotExist:
            raise serializers.ValidationError(_("BlockType does not exit."))


class ProgramField(serializers.Field):

    def to_representation(self, value):
        if value:
            return { "id": value.id, "name": value.name }
        return None

    def to_internal_value(self, data):
        try:
            return models.Program.objects.get(pk=data)
        except models.Program.DoesNotExist:
            raise serializers.ValidationError(_("Program does not exit."))


class PhaseField(serializers.Field):

    def to_representation(self, value):
        if value:
            return { "id": value.id, "name": value.name }
        return None

    def to_internal_value(self, data):
        try:
            return models.Phase.objects.get(pk=data)
        except models.Phase.DoesNotExist:
            raise serializers.ValidationError(_("Phase does not exit."))


class WeekField(serializers.Field):

    def to_representation(self, value):
        if value:
            return { "id": value.id, "name": value.name }
        return None

    def to_internal_value(self, data):
        try:
            return models.Week.objects.get(pk=data)
        except models.Week.DoesNotExist:
            raise serializers.ValidationError(_("Week does not exit."))


class DayField(serializers.Field):

    def to_representation(self, value):
        if value:
            return { "id": value.id, "day": value.day, "day_display": value.get_day_display() }
        return None

    def to_internal_value(self, data):
        try:
            return models.Day.objects.get(pk=data)
        except models.Day.DoesNotExist:
            raise serializers.ValidationError(_("Day does not exit."))


class WorkoutField(serializers.Field):

    def to_representation(self, value):
        if value:
            return { "id": value.id, "name": value.name, "location": value.location }
        return None

    def to_internal_value(self, data):
        try:
            return models.Workout.objects.get(pk=data)
        except models.Workout.DoesNotExist:
            raise serializers.ValidationError(_("Workout does not exit."))