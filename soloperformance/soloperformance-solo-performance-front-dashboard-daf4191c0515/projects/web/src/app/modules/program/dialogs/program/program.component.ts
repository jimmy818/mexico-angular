import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'web-program',
  templateUrl: './program.component.html',
  styleUrls: ['./program.component.scss']
})
export class ProgramDialogComponent implements OnInit {

  items: any[] = [
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}, {}] },
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}] },
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}, {}, {}] },
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}, {}] },
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}, {}] },
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}, {}] },
    { id: 1, name: 'Jump & Agility Program', months: 7, weeks: 3, days: 2, phases: [{}, {}, {}] },
  ]
  constructor() { }

  ngOnInit(): void {
  }

}
