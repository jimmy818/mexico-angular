import { Component, Input, OnInit, Output, EventEmitter, ViewChild, ElementRef } from '@angular/core';

import { WeekDays } from './../models/week-days';
import { WeekDay } from './../models/week-day';
import { Day, Week } from 'sp-core';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  selector: 'sp-weeks-days',
  templateUrl: './weeks-days.component.html',
  styleUrls: ['./weeks-days.component.scss']
})
export class WeeksDaysComponent implements OnInit {

  @Input() weeks: Array<WeekDays> = [];

  @Output() change = new EventEmitter<Array<WeekDays>>();

  @ViewChild('newWeek') newWeekRef: ElementRef;

  get newWeek(): HTMLElement {
    return this.newWeekRef ? this.newWeekRef.nativeElement : null;
  }

  week: Week = new Week();

  constructor() { }

  ngOnInit(): void { }

  dayClick(day: WeekDay): void {
    // Cambia estado de día
    day.selected = !day.selected;
    // Si el último registro NO tiene días seleccionados, se elimina automáticamente.
    // La verificación la realiza hasta que se encuentra alguna semana con algún día seleccionado.
    if (!day.selected) {
      while (this.weeks.length > 0 &&
        !this.weeks[this.weeks.length - 1].checkDaySelected()
      ) {
        this.weeks.splice(this.weeks.length - 1, 1);
      }
    }
    // Indica un cambio en semana/día
    this.weekChanged();
  }

  addWeek(day: Day): void {
    let week = new WeekDays();
    week.selectDay(day);
    this.weeks.push(week);
    this.weekChanged();
    setTimeout(() => {
      if (this.newWeek) {
        this.newWeek.scrollIntoView({ behavior: 'smooth' });
      }
    }, 0);
  }

  removeWeek(index: number): void {
    this.weeks.splice(index, 1);
    this.weekChanged();
  }

  dropWeek(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.weeks, event.previousIndex, event.currentIndex);
  }

  private weekChanged(): void {
    this.change.emit(this.weeks);
  }
}