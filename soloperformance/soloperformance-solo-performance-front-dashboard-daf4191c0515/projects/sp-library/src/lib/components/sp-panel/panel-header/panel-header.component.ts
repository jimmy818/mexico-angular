import { Component, OnInit, TemplateRef, ViewChild } from '@angular/core';

@Component({
  selector: 'sp-panel-header',
  templateUrl: './panel-header.component.html',
  styleUrls: ['./panel-header.component.scss']
})
export class PanelHeaderComponent implements OnInit {

  @ViewChild(TemplateRef) content: TemplateRef<any>;

  constructor() { }

  ngOnInit(): void {
  }
}