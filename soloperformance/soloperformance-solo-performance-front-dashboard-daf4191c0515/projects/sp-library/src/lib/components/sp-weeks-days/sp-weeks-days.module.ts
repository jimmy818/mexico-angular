import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { DragDropModule } from '@angular/cdk/drag-drop';

import { DayPipe } from './pipes/day.pipe';
import { WeeksDaysComponent } from './weeks-days/weeks-days.component';

@NgModule({
  declarations: [
    DayPipe,
    WeeksDaysComponent
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    DragDropModule
  ],
  exports: [
    DayPipe,
    WeeksDaysComponent
  ]
})
export class SpWeeksDaysModule { }
