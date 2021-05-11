import { Component, Input, OnInit, TemplateRef, ViewChild } from '@angular/core';

import { HeaderGroupAlignment } from '../enums/header-group-alignment.enum';

@Component({
  selector: 'sp-header-group',
  templateUrl: './header-group.component.html',
  styleUrls: ['./header-group.component.scss']
})
export class HeaderGroupComponent implements OnInit {

  @Input() expanded = false;
  @Input() alignment = HeaderGroupAlignment.left;
  @Input() isTitle = false;

  @ViewChild(TemplateRef) groupContent: TemplateRef<any>;

  constructor() { }

  ngOnInit(): void {
  }

}
