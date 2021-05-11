import { AfterContentInit, Component, ContentChild, Input, OnInit } from '@angular/core';

import { CollapsableDirection } from './enums/collapsable-direction.enum';
import { PanelBodyComponent } from './panel-body/panel-body.component';
import { PanelHeaderComponent } from './panel-header/panel-header.component';

@Component({
  selector: 'sp-panel',
  templateUrl: './panel.component.html',
  styleUrls: ['./panel.component.scss']
})
export class PanelComponent implements OnInit, AfterContentInit {

  @Input() collapsable = false;
  @Input() collapsableDirection = CollapsableDirection.right;

  @ContentChild(PanelHeaderComponent) headerComponent: PanelHeaderComponent;
  @ContentChild(PanelBodyComponent) bodyComponent: PanelBodyComponent;

  header: PanelHeaderComponent;
  body: PanelBodyComponent;

  collapsed = false;

  constructor() { }

  ngOnInit(): void {
  }

  ngAfterContentInit(): void {
    setTimeout(() => {
      this.header = this.headerComponent;
      this.body = this.bodyComponent;
    }, 0);
  }

  expandCollapse(): void {
    this.collapsed = !this.collapsed;
  }
}
