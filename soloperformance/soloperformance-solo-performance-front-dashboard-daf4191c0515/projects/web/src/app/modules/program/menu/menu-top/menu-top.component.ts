import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'program-menu-top',
  templateUrl: './menu-top.component.html',
  styleUrls: ['./menu-top.component.scss']
})
export class MenuTopComponent implements OnInit {

  @Input() phases: any[] = []

  constructor() { }

  ngOnInit(): void {
  }

}
