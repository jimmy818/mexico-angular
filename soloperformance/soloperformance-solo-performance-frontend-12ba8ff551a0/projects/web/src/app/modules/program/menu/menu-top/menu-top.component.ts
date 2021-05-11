import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'program-menu-top',
  templateUrl: './menu-top.component.html',
  styleUrls: ['./menu-top.component.scss']
})
export class MenuTopComponent implements OnInit {

  phase: any[] = [
    { id: 1, name: 'Strenght Upper/Lower', weeks: 5, number: 375, active: false },
    { id: 2, name: 'Strenght Upper/Lower', weeks: 3, number: 70, active: false },
    { id: 3, name: 'Strenght Upper/Lower', weeks: 4, number: 234, active: false },
    // { id: 4, name: 'Strenght Upper/Lower', weeks: 5, number: 264 },
    // { id: 5, name: 'Strenght Upper/Lower', weeks: 5, number: 375 },
    // { id: 6, name: 'Strenght Upper/Lower', weeks: 3, number: 70 },
    // { id: 7, name: 'Strenght Upper/Lower', weeks: 4, number: 234 },
    // { id: 8, name: 'Strenght Upper/Lower', weeks: 5, number: 264 },
  ]

  constructor() { }

  ngOnInit(): void {
  }

}
