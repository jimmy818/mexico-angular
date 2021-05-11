from enum import Enum


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return tuple((x.value, x.name) for x in cls)



class UserRole(ChoiceEnum):
    SUPER_ADMIN = 1
    INSTITUTION_MANAGER = 2
    STRENGTH_COACH = 3
    ATHLETE = 4

class TypeSubparameters(ChoiceEnum):
    NUM = 1
    NUMERIC_CATALOG = 2
    TIME = 3
    CHOICE = 4
    PERCENTAGE = 5
    CHARACTER_OF_EFFORT = 6
    PERCENTAGE_CATALOG = 7
    DECIMAL = 8

class TypeValueExersiceBlock(ChoiceEnum):
    WARMUP = 1
    FAILURE = 2
    DROPSET = 3
    DEFAULT = 4

class TypeQuestion(ChoiceEnum):
    TEXT = 1
    TIME = 2
    INTEGER = 3

class TypeSurvey(ChoiceEnum):
    PRE = 1
    POST = 2


class TypeSubcription(ChoiceEnum):
    TRIAL = 1
    PAYING = 2
    DEMOS = 3


class Currency(ChoiceEnum):
    EUR = 1
    USD = 2
    MXN = 3
    
class Gender(ChoiceEnum):
    FEMALE = 1
    MALE = 2
    OTHER = 3
    
    
class NivelsQuantityExercise(ChoiceEnum):
    Beginner = 0
    Intermediate = 9
    Advanced = 17    
    Athlete = 25
    Elite  = 49