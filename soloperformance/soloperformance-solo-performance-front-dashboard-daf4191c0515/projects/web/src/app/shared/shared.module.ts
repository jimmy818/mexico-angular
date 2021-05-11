import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

import { SpCardModule, SpHeaderModule, SpInputSearchModule, SpLibraryModule } from 'sp-library';

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
    SpHeaderModule,
    SpInputSearchModule,
    SpCardModule,
    SpLibraryModule,
    RouterModule
  ],
  exports: [
    CommonModule,
    MaterialModule,
    SpHeaderModule,
    SpInputSearchModule,
    SpCardModule,
    SpLibraryModule,
    components,
    directives
  ]
})
export class SharedModule { }
