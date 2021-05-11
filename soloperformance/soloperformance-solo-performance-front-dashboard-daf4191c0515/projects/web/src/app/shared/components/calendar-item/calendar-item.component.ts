import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'web-calendar-item',
  templateUrl: './calendar-item.component.html',
  styleUrls: ['./calendar-item.component.scss']
})
export class CalendarItemComponent implements OnInit {

  @Input() hasIndicator = false;

  constructor() { }

  ngOnInit(): void {
  }

}
