import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';

import { SpDialogModule } from 'sp-dialog';
import { CalendarItemModule } from '../calendar-item/calendar-item.module';

import { EventsComponent } from './events.component';

const COMPONENTS = [
  EventsComponent
];

@NgModule({
  declarations: [
    COMPONENTS
  ],
  imports: [
    CommonModule,
    MatDialogModule,
    MatButtonModule,
    CalendarItemModule,
    SpDialogModule
  ],
  exports: [
    COMPONENTS
  ]
})
export class EventsModule { }