import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';

import { InputSearchComponent } from './input-search.component';

const COMPONENTS = [
  InputSearchComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    MatIconModule,
    FormsModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class SpInputSearchModule { }
