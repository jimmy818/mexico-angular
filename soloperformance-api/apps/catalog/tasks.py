import copy
from . import models


def program_as_library(instance, parent=None):
    program = copy.deepcopy(instance)
    program.pk = None
    program.created_by = None
    program.updated_by = None
    program.has_library = True
    program.request_library = False if parent else True
    program.save()

    for phase in instance.program_phase.filter(active=True):
        week_as_library(phase, program)


def phase_as_library(instance, parent=None):
    phase = copy.deepcopy(instance)
    phase.pk = None
    phase.program = parent if parent else None
    phase.created_by = None
    phase.updated_by = None
    phase.has_library = True
    phase.request_library = False if parent else True
    phase.save()

    for week in instance.phase_week.filter(active=True):
        week_as_library(week, phase)


def week_as_library(instance, parent=None):
    week = copy.deepcopy(instance)
    week.pk = None
    week.phase = parent if parent else None
    week.created_by = None
    week.updated_by = None
    week.has_library = True
    week.request_library = False if parent else True
    week.save()

    for day in instance.week_day.filter(active=True):
        day_as_library(day, week)


def day_as_library(instance, parent=None):
    day = copy.deepcopy(instance)
    day.pk = None
    day.date = None
    day.week = parent if parent else None
    day.created_by = None
    day.updated_by = None
    day.has_library = True
    day.request_library = False if parent else True
    day.save()

    for workout in instance.day_workout.filter(active=True):
        workout_as_library(workout, day)


def workout_as_library(instance, parent=None):
    workout = copy.deepcopy(instance)
    workout.pk = None
    workout.day = parent if parent else None
    workout.created_by = None
    workout.updated_by = None
    workout.has_library = True
    workout.request_library = False if parent else True
    workout.save()

    for block in instance.block_workout.filter(active=True):
        block_as_library(block, workout)


def block_as_library(instance, parent=None):
    block = copy.deepcopy(instance)
    block.pk = None
    block.workout = parent if parent else None
    block.created_by = None
    block.updated_by = None
    block.has_library = True
    block.request_library = False if parent else True
    block.save()

    for exercise in instance.exercises.filter(active=True):
        exercise_as_library(exercise, block)


def exercise_as_library(instance, parent=None):    
    exercise = copy.deepcopy(instance)
    exercise.pk = None
    exercise.block = parent if parent else None
    exercise.created_by = None
    exercise.updated_by = None
    exercise.has_library = True
    exercise.request_library = False if parent else True
    exercise.save()


def block_exercice_library(instance, request,library=False,block=None):
    '''
    exercise
    block
    comment
    active
    created_at
    created_by
    updated_at
    updated_by
    institution
    has_library
    '''
    if block:
        models.ExerciseBlock.objects.filter(block=block).delete()
    new_exersice_block = copy.deepcopy(instance)
    new_exersice_block.pk = None
    new_exersice_block.block = None if library else block
    new_exersice_block.created_by = request.user
    new_exersice_block.updated_by = request.user
    new_exersice_block.institution = request.user.institution
    new_exersice_block.has_library = library
    new_exersice_block.save()

    exersice_catalog = models.ExerciseBlockRelatedCatalog.objects.filter(exercise_block=instance)
    for item in exersice_catalog:
        block_related_library(item,new_exersice_block)




def block_related_library(instance,new_item):
    new_exersice_block_item = copy.deepcopy(instance)
    new_exersice_block_item.pk = None
    new_exersice_block_item.exercise_block = new_item
    new_exersice_block_item.save()

    values_exersice_catalog = models.ItemExerciseBlockRelatedCatalog.objects.filter(catalog=instance)
    print(values_exersice_catalog)
    for item in values_exersice_catalog:
        values_item_block_related(item,new_exersice_block_item)

def values_item_block_related(instance,new_item):
    value_exercice = copy.deepcopy(instance)
    value_exercice.pk = None
    value_exercice.catalog = new_item
    value_exercice.save()
    






