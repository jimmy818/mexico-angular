import { Component, OnInit, ViewChild, TemplateRef } from '@angular/core';

@Component({
  selector: 'sp-panel-body',
  templateUrl: './panel-body.component.html',
  styleUrls: ['./panel-body.component.scss']
})
export class PanelBodyComponent implements OnInit {

  @ViewChild(TemplateRef) content: TemplateRef<any>;

  constructor() { }

  ngOnInit(): void {
  }

}
