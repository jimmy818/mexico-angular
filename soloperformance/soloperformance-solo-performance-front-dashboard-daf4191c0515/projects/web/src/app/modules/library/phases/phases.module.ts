import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';

import { SpInputSearchModule, SpHeaderModule, SpCardModule } from 'sp-library';

import { PhasesRoutingModule } from './phases-routing.module';
import { PhasesComponent } from './phases.component';
import { PhaseListComponent } from './phase-list/phase-list.component';

const COMPONENTS = [
  PhasesComponent,
  PhaseListComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    PhasesRoutingModule,
    MatButtonModule,
    SpInputSearchModule,
    SpHeaderModule,
    SpCardModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class PhasesModule { }
