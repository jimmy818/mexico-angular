import { Component, OnInit, ViewEncapsulation } from '@angular/core';
import { MatDialog } from '@angular/material/dialog';

import { WeekDays } from 'sp-library';

import { BlockCoding, Workout } from '@web/shared/models';
import { WorkoutService } from '@web/shared/services/workout.service';
import { WorkoutAddComponent } from './../workout-add/workout-add.component';
import { Day } from 'sp-core';
import { WorkoutWeeksDaysComponent } from './../workout-weeks-days/workout-weeks-days.component';

@Component({
  selector: 'web-workout-detail',
  templateUrl: './workout-detail.component.html',
  styleUrls: ['./workout-detail.component.scss'],
  encapsulation: ViewEncapsulation.None
})
export class WorkoutDetailComponent implements OnInit {

  workouts: Array<Workout> = [];

  categories: Array<BlockCoding> = [];

  exerciseFilterExpanded = false;

  exercises: Array<any> = [];

  weeksDays: Array<WeekDays> = [];

  constructor(
    private dialog: MatDialog,
    private workoutService: WorkoutService
  ) { }

  ngOnInit(): void {

    this.exercises.push({ id: 1, name: 'Equipment', subcategories: [] });
    this.exercises.push({ id: 2, name: 'Tags', subcategories: [] });
    this.exercises.push({ id: 3, name: 'Chains', subcategories: [] });
    this.exercises.push({ id: 4, name: 'Muscle regions', subcategories: [] });
    this.exercises.push({ id: 5, name: 'Laterality', subcategories: [] });
    this.exercises.push({ id: 6, name: 'Limb', subcategories: [] });
    this.exercises.push({ id: 7, name: 'Plane', subcategories: [] });
    this.exercises.push({ id: 8, name: 'Category', subcategories: [] });
    this.exercises.push({ id: 9, name: 'Myofascial release', subcategories: [] });
    this.exercises.push({ id: 9, name: 'Instability', subcategories: [] });
    this.exercises.push({ id: 9, name: 'Weights & resistances', subcategories: [{ id: 1, name: 'Barbell' }, { id: 2, name: 'Med ball' }, { id: 3, name: 'Sandbag' }] });
    this.exercises.push({ id: 9, name: 'Agility & plyo', subcategories: [] });
    this.exercises.push({ id: 9, name: 'Elastic resistance', subcategories: [] });
    this.exercises.push({ id: 9, name: 'Others', subcategories: [] });

    this.workouts.push(new Workout());
    this.workouts.push(new Workout());
    this.workouts.push(new Workout());
    this.workouts.push(new Workout());
    this.workouts.push(new Workout());

    const weekDay = new WeekDays();
    weekDay.selectDay(Day.friday);
    weekDay.selectDay(Day.monday);
    this.weeksDays.push(weekDay);
    this.weeksDays.push(new WeekDays());
    this.weeksDays.push(new WeekDays());

    this.workoutService.getBlockCodings()
      .subscribe(categories => {
        this.categories = categories;
      });
  }

  addWorkoutClick(): void {

    // Visualiza selección de semanas, días.
    const dialogRef = this.dialog.open(WorkoutWeeksDaysComponent, {
      width: '650px',
      data: this.weeksDays
    });

    dialogRef.afterClosed().subscribe(result => {
      if (result) {
        this.weeksDays = result;

        // Visualiza configurador rápido de workout.
        const dialogWorkoutRef = this.dialog.open(WorkoutAddComponent, {
          width: '1132px',
          maxWidth: '85vw'
        });

      }
    })
  }

  viewChange(checked: boolean): void {
    console.log(checked);
  }

  inputSearchFocus(): void {
    console.log('Focus');
    this.exerciseFilterExpanded = true;
  }

  inputSearchBlur(): void {
    console.log('Blur');
    //this.exerciseFilterExpanded = false;
  }


}
