import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { HeaderComponent } from './header.component';
import { HeaderGroupComponent } from './header-group/header-group.component';
import { HeaderIconComponent } from './header-icon/header-icon.component';

const COMPONENTS = [
  HeaderComponent,
  HeaderGroupComponent,
  HeaderIconComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class SpHeaderModule { }
