import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatButtonToggleModule } from '@angular/material/button-toggle';

import { ButtonToggleComponent } from './button-toggle.component';

const COMPONENTS = [
  ButtonToggleComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    MatButtonModule,
    MatButtonToggleModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class SpButtonToggleModule { }