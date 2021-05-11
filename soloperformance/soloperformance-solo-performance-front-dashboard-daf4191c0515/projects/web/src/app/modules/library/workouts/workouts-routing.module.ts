import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WorkoutsComponent } from './workouts.component';
import { WorkoutListComponent } from './workout-list/workout-list.component';

const routes: Routes = [
  {
    path: '',
    component: WorkoutsComponent,
    children: [
      {
        path: '',
        redirectTo: 'my-workouts',
        pathMatch: 'full'
      },
      {
        path: 'all-workouts',
        component: WorkoutListComponent
      },
      {
        path: 'my-workouts',
        component: WorkoutListComponent
      },
      {
        path: 'institutional-workouts',
        component: WorkoutListComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WorkoutsRoutingModule { }
