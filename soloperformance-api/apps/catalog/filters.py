from django.db.models import Q
from django_filters import rest_framework as filters
from . import models


def filter_tab(user, queryset, value):
    if value == 'all':
        return queryset
    if value == 'me':
        return queryset.filter(created_by=user)
    if value == 'institution':
        if user.institution:
            return queryset.filter(created_by__institution=user.institution)

    return queryset


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass


class BlockFilter(filters.FilterSet):
    athletes = NumberInFilter(field_name='athletes', lookup_expr='in')
    # athletes = filters.CharFilter(method='filter_athletes')
    tab = filters.CharFilter(method='filter_tab')

    def filter_athletes(self, queryset, name, value):
        if value:
            return queryset.filter(athletes__in=value)

    def filter_tab(self, queryset, name, value):
        return filter_tab(self.request.user, queryset, value)

    class Meta:
        model = models.Block
        fields = (
            'coding',
            'sub_coding',
            'type',
            'workout',
            'athletes',
            'limit',
            'active',
            'has_library',
            'tab',
        )



class ExerciseFilter(filters.FilterSet):
    sub_category = NumberInFilter(field_name='sub_category', lookup_expr='in')
    list_sub_category = NumberInFilter(field_name='sub_category', lookup_expr='in')
    tab = filters.CharFilter(method='filter_tab')

    def filter_list_sub_category(self, queryset, name, value):
        if value:
            return queryset.filter(sub_category__in=value)
    
    def filter_sub_category(self, queryset, name, value):
        if value:
            return queryset.filter(sub_category=value)

    def filter_tab(self, queryset, name, value):
        user = self.request.user
        if value == 'all':
            return queryset.filter(Q(created_by=user) | Q(created_by__institution=user.institution) | Q(has_library=True))
        if value == 'me':
            return queryset.filter(created_by=user)
        if value == 'institution':
            if user.institution:
                return queryset.filter(created_by__institution=user.institution)

        return queryset 

    # class Meta:
    #     model = models.Exercise
    class Meta:
        model = models.Exercise
        fields = (
            'sub_category',
            'created_by',
            'created_by__institution',
            'active',
            'has_library',
            'request_library',
            'list_sub_category',
            'sub_category__category',
            'sub_category__category__category_level',
            'tab'
        )


class ProgramLibraryFilter(filters.FilterSet):
    athletes = NumberInFilter(field_name='athletes', lookup_expr='in')
    tab = filters.CharFilter(method='filter_tab')

    def filter_tab(self, queryset, name, value):
        return filter_tab(self.request.user, queryset, value)

    class Meta:
        model = models.Program
        fields = (
            'team',
            'athletes',
            'active',
            'has_library',
            'tab',
        )


class PhaseLibraryFilter(filters.FilterSet):
    tab = filters.CharFilter(method='filter_tab')

    def filter_tab(self, queryset, name, value):
        return filter_tab(self.request.user, queryset, value)

    class Meta:
        model = models.Phase
        fields = (
            'program',
            'active',
            'has_library',
            'tab',
        )


class WorkoutLibraryFilter(filters.FilterSet):
    tab = filters.CharFilter(method='filter_tab')

    def filter_tab(self, queryset, name, value):
        user = self.request.user
        if value == 'all':
            return queryset
        if value == 'me':
            return queryset.filter(created_by=user)
        if value == 'institution':
            if user.institution:
                return queryset.filter(institution=user.institution)
        return queryset 

    class Meta:
        model = models.Workout
        fields = (
            'day',
            'start_time',
            'end_time',
            'active',
            'tab',
        )
