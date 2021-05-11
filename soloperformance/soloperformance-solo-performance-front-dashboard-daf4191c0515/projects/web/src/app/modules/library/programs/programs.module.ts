import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpCardModule, SpHeaderModule, SpInputSearchModule } from 'sp-library';

import { ProgramsRoutingModule } from './programs-routing.module';
import { ProgramsComponent } from './programs.component';
import { ProgramListComponent } from './program-list/program-list.component';
import { ProgramDetailComponent } from './program-detail/program-detail.component';

const COMPONENTS = [
  ProgramsComponent,
  ProgramListComponent,
  ProgramDetailComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    ProgramsRoutingModule,
    MatButtonModule,
    SpInputSearchModule,
    SpCardModule,
    SpHeaderModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class ProgramsModule { }
