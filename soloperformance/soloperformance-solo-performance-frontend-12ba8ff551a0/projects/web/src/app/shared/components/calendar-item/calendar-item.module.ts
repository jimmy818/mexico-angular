import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CalendarItemComponent } from './calendar-item.component';

const COMPONENTS = [
  CalendarItemComponent
]

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule
  ],
  exports:[
    ...COMPONENTS
  ]
})
export class CalendarItemModule { }
