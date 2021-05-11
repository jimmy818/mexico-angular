import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SpDialogModule } from 'sp-dialog';
import { SharedModule } from '@web/shared/shared.module';
import { ProgramDialogComponent } from './program/program.component';
import { PhaseDialogComponent } from './phase/phase.component';
import { AssignProgramComponent } from './assign-program/assign-program.component';
import { SpInputSearchModule } from 'sp-library';

const COMPONENTS = [
  ProgramDialogComponent,
  PhaseDialogComponent,
  AssignProgramComponent
];

@NgModule({
  declarations: [
    ...COMPONENTS
  ],
  imports: [
    CommonModule,
    SpDialogModule,
    SharedModule,
    SpInputSearchModule
  ],
  exports: [
    ...COMPONENTS
  ]
})
export class DialogsModule { }
