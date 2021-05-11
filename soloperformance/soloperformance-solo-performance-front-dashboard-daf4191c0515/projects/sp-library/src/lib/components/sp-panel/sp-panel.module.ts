import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { PanelComponent } from './panel.component';
import { PanelHeaderComponent } from './panel-header/panel-header.component';
import { PanelBodyComponent } from './panel-body/panel-body.component';


const COMPONENTS = [
  PanelComponent,
  PanelHeaderComponent,
  PanelBodyComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    MatButtonModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class SpPanelModule { }
