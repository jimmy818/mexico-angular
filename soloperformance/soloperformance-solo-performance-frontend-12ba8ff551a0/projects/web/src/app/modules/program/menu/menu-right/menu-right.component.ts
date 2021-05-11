import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'program-menu-right',
  templateUrl: './menu-right.component.html',
  styleUrls: ['./menu-right.component.scss']
})
export class MenuRightComponent implements OnInit {

  weeks: number[] = [80, 70, 35, 16, 25];

  constructor() { }

  ngOnInit(): void {
  }

}
