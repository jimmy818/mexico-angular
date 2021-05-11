import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'sp-header-icon',
  templateUrl: './header-icon.component.html',
  styleUrls: ['./header-icon.component.scss']
})
export class HeaderIconComponent implements OnInit {

  @ViewChild(TemplateRef) logoContent: TemplateRef<any>;

  constructor() { }

  ngOnInit(): void {
  }

}
