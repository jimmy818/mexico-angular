import { Component, Inject, OnInit } from '@angular/core';
import { MAT_DIALOG_DATA } from '@angular/material/dialog';
import { EventsDialogData } from './events-dialog-data.interface';

@Component({
  selector: 'web-events',
  templateUrl: './events.component.html',
  styleUrls: ['./events.component.scss']
})
export class EventsComponent implements OnInit {

  constructor(
    @Inject(MAT_DIALOG_DATA) public data: EventsDialogData
  ) { }

  ngOnInit(): void { }
}