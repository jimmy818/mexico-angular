import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { MatMenuModule } from '@angular/material/menu';
import { MatButtonModule } from '@angular/material/button';
import { MatSelectModule } from '@angular/material/select';
import { MatCheckboxModule } from '@angular/material/checkbox';
import { MatListModule } from '@angular/material/list';
import { MatTooltipModule } from '@angular/material/tooltip';
import { MatIconModule } from '@angular/material/icon';
import { MatDialogModule } from '@angular/material/dialog';

import { SpDialogModule } from 'sp-dialog';
import { SpPanelModule, SpHeaderModule, SpInputSearchModule, SpButtonToggleModule, SpMenuModule, SpCardModule, SpClickStopPropagationModule, SpWeeksDaysModule } from 'sp-library';

import { ImgsModule } from '@web/shared/components/imgs/imgs.module';

import { WorkoutCreateRoutingModule } from './workout-builder-routing.module';
import { WorkoutBuilderComponent } from './workout-builder.component';
import { WorkoutDetailComponent } from './workout-detail/workout-detail.component';
import { WorkoutDayComponent } from './workout-day/workout-day.component';
import { WorkoutAddComponent } from './workout-add/workout-add.component';
import { WorkoutWeeksDaysComponent } from './workout-weeks-days/workout-weeks-days.component';

const COMPONENTS = [
  WorkoutBuilderComponent,
  WorkoutDetailComponent,
  WorkoutDayComponent,
  WorkoutAddComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS,
    WorkoutWeeksDaysComponent
  ],
  imports: [
    CommonModule,
    WorkoutCreateRoutingModule,
    ReactiveFormsModule,
    MatMenuModule,
    MatButtonModule,
    MatSelectModule,
    MatCheckboxModule,
    MatListModule,
    MatTooltipModule,
    MatIconModule,
    MatCheckboxModule,
    MatDialogModule,
    SpInputSearchModule,
    SpHeaderModule,
    SpCardModule,
    SpPanelModule,
    SpDialogModule,
    SpButtonToggleModule,
    SpMenuModule,
    SpClickStopPropagationModule,
    SpWeeksDaysModule,
    ImgsModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class WorkoutBuilderModule { }
