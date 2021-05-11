import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { ExercisesComponent } from './exercises.component';
import { ExerciseListComponent } from './exercise-list/exercise-list.component';

const routes: Routes = [
  {
    path: '',
    component: ExercisesComponent,
    children: [
      { path: '', redirectTo: 'my-exercises', pathMatch: 'full' },
      {
        path: 'all-exercises',
        component: ExerciseListComponent
      },
      {
        path: 'my-exercises',
        component: ExerciseListComponent
      },
      {
        path: 'institutional-exercises',
        component: ExerciseListComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class ExercisesRoutingModule { }
