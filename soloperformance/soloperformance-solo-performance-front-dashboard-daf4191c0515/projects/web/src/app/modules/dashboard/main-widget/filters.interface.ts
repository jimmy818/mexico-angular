import { Filter } from './filter-value.interface';

export interface Filters {
    periods: Filter;
    programs: Filter;
    phases: Filter;
    events: Filter;
    dailyLoad: Filter;
    workouts: Filter;
    exercisesNumber: Filter;
    totalVolume: Filter;
    rpe: Filter;
    preTrainingSurvey: Filter;
    sessionTime: Filter;
}