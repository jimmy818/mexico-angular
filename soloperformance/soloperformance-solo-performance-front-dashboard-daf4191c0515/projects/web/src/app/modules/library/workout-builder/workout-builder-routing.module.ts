import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import { WorkoutBuilderComponent } from './workout-builder.component';
import { WorkoutDetailComponent } from './workout-detail/workout-detail.component';

const routes: Routes = [
  {
    path: '',
    component: WorkoutBuilderComponent,
    children: [
      { path: '', redirectTo: 'create', pathMatch: 'full' },
      {
        path: 'create',
        component: WorkoutDetailComponent
      }
    ]
  }
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class WorkoutCreateRoutingModule { }
