import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpInputSearchModule, SpHeaderModule, SpCardModule } from 'sp-library';

import { WorkoutsRoutingModule } from './workouts-routing.module';
import { WorkoutsComponent } from './workouts.component';
import { WorkoutListComponent } from './workout-list/workout-list.component';

const COMPONENTS = [
  WorkoutsComponent,
  WorkoutListComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS,
  ],
  imports: [
    CommonModule,
    WorkoutsRoutingModule,
    MatButtonModule,
    SpHeaderModule,
    SpCardModule,
    SpInputSearchModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class WorkoutsModule { }
