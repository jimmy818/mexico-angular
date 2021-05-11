import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'program-menu-left',
  templateUrl: './menu-left.component.html',
  styleUrls: ['./menu-left.component.scss']
})
export class MenuLeftComponent implements OnInit {

  phase: any[] = [
    // {
    //   name: 'Strenght Upper/Lower',
    //   weeks: [
    //     {},
    //     {},
    //   ]
    // },
    {
      name: 'Strenght Upper/Lower',
      active: 0,
      weeks: [
        { id: 1 },
        { id: 2 },
        { id: 3 },
        { id: 4 },
        { id: 5 }
      ]
    }
  ]

  constructor() { }

  ngOnInit(): void {
  }

}
