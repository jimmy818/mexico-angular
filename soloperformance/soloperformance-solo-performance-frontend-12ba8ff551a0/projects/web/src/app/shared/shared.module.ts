import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { SpLibraryModule } from 'sp-library';

import { HeaderComponent } from './components/header/header.component';
import { MaterialModule } from '../material/material.module';

const components = [
  HeaderComponent
];

const directives = [
];

@NgModule({
  declarations: [
    components,
    directives
  ],
  imports: [
    CommonModule,
    MaterialModule,
    SpLibraryModule,
    RouterModule
  ],
  exports: [
    CommonModule,
    MaterialModule,
    SpLibraryModule,
    components,
    directives
  ]
})
export class SharedModule { }
