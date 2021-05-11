import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpInputSearchModule, SpHeaderModule, SpCardModule } from 'sp-library';

import { ExercisesRoutingModule } from './exercises-routing.module';
import { ExercisesComponent } from './exercises.component';
import { ExerciseListComponent } from './exercise-list/exercise-list.component';

const COMPONENTS = [
  ExercisesComponent,
  ExerciseListComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    ExercisesRoutingModule,
    MatButtonModule,
    SpInputSearchModule,
    SpHeaderModule,
    SpCardModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class ExercisesModule { }
