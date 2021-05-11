from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register('categories-level', views.LevelCategoryViewSet)
router.register('categories', views.CategoryViewSet)
router.register('subcategories', views.SubCategoryViewSet)
router.register('exercises', views.ExcercicesViewSet)
router.register('exercises-image', views.ExerciceImageView)
router.register('programs', views.ProgramViewSet)
router.register('phases', views.PhaseViewSet)
# router.register('weeks', views.WeekViewSet)
router.register('weeks', views.WeekPhaseViewSet)
# router.register('days', views.DayViewSet)
router.register('days', views.DayWeekViewSet)
router.register('workouts', views.WorkoutViewSet)
router.register('blocktypes', views.BlockTypeViewSet)
router.register('blocks', views.BlockViewSet)
router.register('coding', views.CodingView)
router.register('coding-sub', views.CodingCategoryView)
router.register('block-exercises', views.BlockExerciceView)
router.register('block-exercises-catalog', views.BlockExerciseCatalogView)
router.register('sub-block-exercises-catalog', views.BlockExerciseCatalogSubparameterView)
router.register('item-block-exercises-catalog', views.ExerciseBlockRelatedCatalogView)
router.register('values-block-exercises-catalog', views.ItemExerciseBlockRelatedCatalogView)
router.register('program-library', views.ProgramLibraryViewSet)
router.register('phase-library', views.PhaseLibraryViewSet)
router.register('workout-library', views.WorkoutLibraryViewSet)
router.register('block-library', views.BlockLibraryViewSet)
router.register('row-block-value', views.RowBlockTypeView)
router.register('category-equipment', views.CategoryEquipmentView)



urlpatterns = [
    path('excel/', views.ExcelCategory.as_view()),
    path('excel-exercises/', views.ExcelExcercices.as_view()),
    path('program-phase-detail/', views.ProgramPhaseDetail.as_view()),
    # path('weeks-sorting/<int:phase>/', views.WeeksSorting.as_view()),

    ## ORDERING PROGRAM ITEMS
    path('weeks-sorting/<int:phase>/', views.ArrayWeeksSorting.as_view()),
    path('workouts-sorting/<int:day>/', views.ArrayWorkoutksSorting.as_view()),
    path('blocks-sorting/<int:workout>/', views.ArrayBlocksSorting.as_view()),


    path('create-move-phases/', views.CreateAndMovePhases.as_view()),
    path('delete-move-phases/<int:pk>/', views.DeleteAndMovePhases.as_view()),
    path('create-move-weeks/', views.CreateAndMoveWeeks.as_view()),
    path('delete-move-weeks/<int:pk>/', views.DeleteAndMoveWeeks.as_view()),
    path('copy-weeks/<int:pk>/', views.CopyWeeks.as_view()),
    path('phases-sorting/<int:program>/', views.PhaseSorting.as_view()),
    path('all-days-week/<int:phase>/', views.AllDaysWeeks.as_view()),
    path('user-program/<int:program>/', views.UserProgramView.as_view()),
    path('exercise-block-detail/<int:exerciceblock>/', views.ExerciseBlockDetailView.as_view()),
    path('block-values/<int:workout>/', views.BlockDetaillApp.as_view()),
    path('line-block-exercises-catalog/<int:row>/<int:block>/', views.LineExerciseBlockRelatedCatalogView.as_view()),
    path('clone-line-block-exercises-catalog/<int:row>/<int:block>/', views.LineCloneExerciseBlockRelatedCatalogView.as_view()),

    path('workout-calendar', views.WorkoutUserCalendarView.as_view()),
    path('today-workout', views.TodayWorkoutUserCalendarView.as_view()),
    
    path('phases-library-import/<int:program>/', views.PhaseLibraryImportAPIView.as_view()),
    path('workout-library-import/<int:day>/', views.WorkoutLibraryImportAPIView.as_view()),
    path('workout-copy/<int:workout>/', views.WorkoutCopyAPIView.as_view()),
]

urlpatterns += router.urls
