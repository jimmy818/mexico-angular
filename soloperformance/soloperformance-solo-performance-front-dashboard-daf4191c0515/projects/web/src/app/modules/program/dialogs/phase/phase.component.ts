import { Component, OnInit } from '@angular/core';
import { CdkDragDrop, moveItemInArray } from '@angular/cdk/drag-drop';

@Component({
  selector: 'web-phase',
  templateUrl: './phase.component.html',
  styleUrls: ['./phase.component.scss']
})
export class PhaseDialogComponent implements OnInit {

  weeks: any[] = [
    { mon: false, tue: true, wed: true, thu: false, fri: true, sat: false, sun: false },
    { mon: true, tue: true, wed: false, thu: false, fri: true, sat: true, sun: true },
    { mon: false, tue: false, wed: true, thu: true, fri: true, sat: true, sun: true },
    { mon: false, tue: false, wed: true, thu: true, fri: false, sat: true, sun: false },
    { mon: true, tue: true, wed: true, thu: false, fri: false, sat: false, sun: false }
  ]
  constructor() { }

  ngOnInit(): void {
  }

  addNew(day: number): void {
    let week = { mon: false, tue: false, wed: false, thu: false, fri: false, sat: false, sun: false }
    switch (day) {
      case 1: week.mon = true; break;
      case 2: week.tue = true; break;
      case 3: week.wed = true; break;
      case 4: week.thu = true; break;
      case 5: week.fri = true; break;
      case 6: week.sat = true; break;
      case 7: week.sun = true; break;
    }
    this.weeks.push(week);
  }

  drop(event: CdkDragDrop<string[]>) {
    moveItemInArray(this.weeks, event.previousIndex, event.currentIndex);
  }
}
