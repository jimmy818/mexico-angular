import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpHeaderModule } from 'sp-library';

import { LibraryRoutingModule } from './library-routing.module';
import { LibraryComponent } from './library.component';

const COMPONENTS = [
  LibraryComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    LibraryRoutingModule,
    MatButtonModule,
    SpHeaderModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class LibraryModule { }
